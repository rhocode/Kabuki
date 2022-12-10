#!/usr/bin/env python
# Main kabuki.py
# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import json
import queue
import threading
import time

from flask import Flask, render_template, request, send_from_directory, url_for
from PIL import Image, ImageDraw, ImageFile

from rgbmatrix import graphics

from animation import Animation
from face import Face
from utils import command_restart, command_shutdown, command_shutdown_cancel

ImageFile.LOAD_TRUNCATED_IMAGES = True

# constants used throughout project
WIDTH = 32
HEIGHT = 32
SPEED = 1.0 / 30.0
IDLE_TIME = 50
EYES = 0
MOUTHS = 16


class Kabuki:
    def __init__(self, matrix):
        self.matrix = matrix
        # self.flask_app = flask_app
        self.face = Face()
        self.eye_queue = queue.Queue()
        self.mouth_queue = queue.Queue()
        self.eye_latch = self.face.eyes["blink"].get_latched()
        self.mouth_latch = self.face.mouths["idle_mouth"].get_latched()
        self.last_eye = None
        self.last_mouth = None

        flask_app = Flask(__name__)
        flask_app.use_reloader = False
        flask_app.debug = False

        @flask_app.route("/", methods=["GET"])
        def get_index():
            return render_template(
                "remote.html",
                eyes=[eye for eye in self.face.eyes],
                mouths=[mouth for mouth in self.face.mouths],
            )

        @flask_app.route("/pi", methods=["GET"])
        def get_pi():
            return render_template("pi.html")

        @flask_app.route("/command", methods=["POST"])
        def command():
            json_request = json.loads(request.data)
            print("post command", json_request)
            try:
                if "eye" in json_request:
                    if not self.last_eye == None and self.last_eye != json_request["eye"] and json_request["direction"] != 'l':
                        self.play_seq(self.last_eye, EYES, "r")
                        time.sleep(0.5)
                    self.play_seq(json_request["eye"], EYES, json_request["direction"])
                    self.last_eye = json_request["eye"]
                if "mouth" in json_request:
                    if not self.last_mouth == None and self.last_mouth != json_request["mouth"] and json_request["direction"] != 'l':
                        self.play_seq(self.last_mouth, MOUTHS, "r")
                        time.sleep(0.5)
                    self.play_seq(json_request["mouth"], MOUTHS, json_request["direction"])
                    self.last_mouth = json_request["mouth"]
                if "shutdown" in json_request:
                    if json_request["shutdown"] == "confirm":
                        command_shutdown()
                    elif json_request["shutdown"] == "cancel":
                        command_shutdown_cancel()
                if "restart" in json_request:
                    if json_request["shutdown"] == "confirm":
                        command_restart()
            except KeyError as e:
                return {"error": str(e), "type": "KeyError"}
            except Exception as e:
                print("Command Exception: ", e)
                return {"error": "Internal Server Error"}
            return {"eye": self.eye_latch.key, "mouth": self.mouth_latch.key}

        @flask_app.route("/status", methods=["GET"])
        def get_status():
            return {"eye": self.eye_latch.key, "mouth": self.mouth_latch.key}

        @flask_app.route("/list", methods=["GET"])
        def get_list():
            return {
                "eyes": [eye for eye in self.face.eyes],
                "mouths": [mouth for mouth in self.face.mouths],
            }

        def run_flask():
            flask_app.run(host="0.0.0.0", use_reloader=False)
            flask_app.add_url_rule("/favicon.ico",
                                   redirect_to=url_for("static", filename="icon.png"))

        # flask listener is a seperate thread
        t = threading.Thread(target=run_flask, daemon=True)
        t.start()

        # start the render loop on main thread
        self.eye_loop_flag = False
        self.mouth_loop_flag = False
        self.render_loop()

    def play_seq(self, expression, board, direction):
        # add sequence to correct queue and reverse if needed
        used_queue = None
        seq_source = None

        if board == EYES:
            used_queue = self.eye_queue
            seq_source = self.face.eyes
            if direction == 'l':
                self.eye_loop_flag = True
            else:
                self.eye_loop_flag = False
        else:
            used_queue = self.mouth_queue
            seq_source = self.face.mouths
            if direction == 'l':
                self.mouth_loop_flag = True
            else:
                self.mouth_loop_flag = False

        sequence = seq_source[expression]

        if direction == "r":
            sequence = sequence.get_reversed()

        used_queue.put(sequence)

    def play_hold(self, hold, board, duration=IDLE_TIME):
        # generate a bunch of frames to hold
        hold_seq = Animation(
            "hold_" + hold,
            [self.face.hold_frames[hold] for i in range(duration)])

        if board == EYES:
            self.eye_queue.put(hold_seq)
        else:
            self.mouth_queue.put(hold_seq)

    def compute_eyes(self):
        idx = 0
        # default hold is no expression from blink
        self.current_eye = self.eye_latch
        while True:
            if self.eye_queue.empty() and len(self.current_eye) == idx:
                # reset
                idx = 0
                if not self.eye_loop_flag:
                    self.current_eye = self.eye_latch

            elif not self.eye_queue.empty():
                self.current_eye = self.eye_queue.get()
                if self.current_eye.is_latch():
                    self.eye_latch = self.current_eye.get_latched()
                idx = 0
            #print(self.current_eye, idx)
            yield self.current_eye[idx]
            idx += 1

    def compute_mouth(self):
        idx = 0
        # default hold is a line from smile_closed
        self.current_mouth = self.mouth_latch
        while True:
            if self.mouth_queue.empty() and len(self.current_mouth) == idx:
                # reset
                idx = 0
                self.current_mouth = self.mouth_latch
            elif not self.mouth_queue.empty():
                self.current_mouth = self.mouth_queue.get()
                if self.current_mouth.is_latch():
                    self.mouth_latch = self.current_mouth.get_latched()
                idx = 0
            yield self.current_mouth[idx]
            idx += 1

    def compute_frame(self):
        eye_frame = self.compute_eyes()
        mouth_frame = self.compute_mouth()

        while True:
            # do work to combine eyes and mouths and yield resulting frame
            frame = Image.new("RGB", (WIDTH, HEIGHT))
            try:
                frame.paste(next(eye_frame), (0, EYES))
            except Exception as e:
                print("Eye Exception:", e)

            try:
                frame.paste(next(mouth_frame), (0, MOUTHS))
            except Exception as e:
                print("Mouth Exception:", e)
            yield frame

    def render_loop(self):
        next_frame = self.compute_frame()
        while True:
            try:
                self.matrix.SetImage(next(next_frame), 0, 0)
                time.sleep(SPEED)
            except Exception as e:
                print("Render Exception:", e)