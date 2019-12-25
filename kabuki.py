#!/usr/bin/env python

# Main kabuki.py

# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import time
import queue
import threading
from rgbmatrix import graphics
from PIL import Image, ImageDraw
from multiprocessing import JoinableQueue, Process

from face import Face

# constants used throughout project
WIDTH = 32
HEIGHT = 32
SPEED = 1.0 / 20.0
IDLE_TIME = 50
EYES = 0
MOUTH = 16

class Kabuki:

    def __init__(self, matrix):
        self.matrix = matrix
        self.face = Face()
        self.eye_queue = queue.Queue()
        self.mouth_queue = queue.Queue()
        self.loop_proc = Process(target=self.loop)
        #self.compute_proc = Process(target=self.compute_frame)
        self.eye_proc = Process(target=self.compute_eyes)
        self.mouth_proc = Process(target=self.compute_mouth)
        self.render_proc = Process(target=self.render_loop)
        t = threading.Thread(target=self.loop)
        t.start()
        #self.reset_face()
        self.render_loop()

    def test_queue(self):
        print('test_queue')
        while 1:
            self.eye_queue.put(1)
            time.sleep(5)
            self.eye_queue.get()
            time.sleep(5)

    def test_draw(self):
        while 1:
            print(self.eye_queue.empty())
            image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
            draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
            # Draw some shapes into image (no immediate effect on matrix)...
            draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))
            draw.line((0, 0, 31, 31), fill=(255, 0, 0))
            draw.line((0, 31, 31, 0), fill=(0, 255, 0))

            # Then scroll image across matrix...
            for n in range(-32, 33):  # Start off top-left, move off bottom-right
                self.matrix.Clear()
                self.matrix.SetImage(image, n, n)
                time.sleep(0.05)

    def start_render(self):
        self.loop_proc.start()
        #self.eye_proc.start()
        #self.mouth_proc.start()
        #self.render_proc.start()


    def play_seq(self, expression, board, direction):
        
        if board == EYES:
            sequence = self.face.eyes[expression]
        else:
            sequence = self.face.mouth[expression]

        if direction == 'r':
            sequence = sequence[::-1]

        if board == EYES:
            self.eye_queue.put(sequence)
        else:
            self.mouth_queue.put(sequence)
        

    def play_hold(self, hold, board):
        hold_seq = [self.face.hold_frames[hold] for i in range(IDLE_TIME)]

        if board == EYES:
            self.eye_queue.put(hold_seq)
        else:
            self.mouth_queue.put(hold_seq)

    def compute_eyes(self):
        idx = 0
        idle_eye_frame = self.face.hold_frames['blink']
        current_eye = [idle_eye_frame]
        while(True):
            if self.eye_queue.empty() and len(current_eye) == idx:
                #reset
                idx = 0
                current_eye = [idle_eye_frame]
            else:
                if not self.eye_queue.empty():
                    current_eye = self.eye_queue.get()
            #print(current_eye, idx)
            yield current_eye[idx]
            idx += 1

    def compute_mouth(self):
        idx = 0
        idle_mouth_frame = self.face.hold_frames['smile_closed']
        current_mouth = [idle_mouth_frame]
        while(True):
            if self.mouth_queue.empty() and len(current_mouth) == idx:
                #reset
                idx = 0
                current_mouth = [idle_mouth_frame]
            else:
                if not self.mouth_queue.empty():
                    current_mouth = self.mouth_queue.get()
            yield current_mouth[idx]
            idx += 1



    def compute_frame(self):
        eye_frame = self.compute_eyes()
        mouth_frame = self.compute_mouth()
        
        while(True):
            # do work to combine eye and mouth and add to render queue
            #print(next(eye_frame), EYES, MOUTH)
            frame = Image.new('RGB', (WIDTH, HEIGHT))
            frame.paste(next(eye_frame), (0, EYES))
            #frame.paste(next(mouth_frame), (0, MOUTH))
            yield frame
            

    def render_loop(self):
        next_frame = self.compute_frame()
        while(True):
            self.matrix.SetImage(next(next_frame), 0, 0)
            time.sleep(SPEED)
        pass


    def reset_face(self):
        self.play_hold(self.face.hold_frames['blink'], EYES)
        self.play_seq(self.face.eyes['blink'], EYES)
        self.play_hold(self.face.hold_idle, EYES)
        self.play_hold(self.face.hold_line, MOUTH)

    def reverse_frames(self, seq):
        return seq[::-1]

    def loop(self):
        while(True):
            self.play_seq('blink', EYES, 'f')
            time.sleep(2)
            self.play_seq('happy', EYES, 'f')
            self.play_hold('happy', EYES)
            self.play_seq('happy', EYES, 'r')
            time.sleep(2)
            
        #self.matrix.Clear()
        # animations with "loop" are standalone loops, but may need to be prefaced
        # by a different state (eg sad first then cry) - if triggered seperately, split out seq
        # unless noted, faces return to neutral

            # ###### EYES #######
            # # idle (blink) loop
            # self.play_hold(self.face.hold_idle, EYES)
            # self.play_seq(self.face.eyes['blink'], EYES)
            # self.play_hold(self.face.hold_idle, EYES)
            
            # # happy
            # self.play_seq(self.face.eyes['happy'], EYES)
            # self.play_hold(self.face.hold_happy, EYES)
            # self.play_seq(reversed(self.face.eyes['happy']), EYES)
            
            # # sad
            # self.play_seq(self.face.eyes['sad'], EYES)
            # self.play_hold(self.face.hold_sad, EYES)
            # self.play_seq(reversed(self.face.eyes['sad']), EYES)
            
            # # cry loop (return to sad)
            # self.play_seq(self.face.eyes['sad'], EYES)
            # self.play_seq(self.face.eyes['cry'], EYES)
            # self.play_seq(self.face.eyes['cry'], EYES)
            # self.play_seq(self.face.eyes['cry'], EYES)
            # self.play_seq(reversed(self.face.eyes['sad']), EYES)
            
            # # angry
            # self.play_seq(self.face.eyes['angry'], EYES)
            # self.play_hold(self.face.hold_angry, EYES)
            # self.play_seq(reversed(self.face.eyes['angry']), EYES)

            # # suspicious
            # self.play_seq(self.face.eyes['suspicious'], EYES)
            # self.play_hold(self.face.hold_suspicious, EYES)
            # self.play_seq(reversed(self.face.eyes['suspicious']), EYES)

            # # sleep
            # self.play_seq(self.face.eyes['sleep'], EYES)
            # self.play_hold(self.face.hold_sleep, EYES)
            # self.play_seq(reversed(self.face.eyes['sleep']), EYES)

            # # surprise
            # self.play_seq(self.face.eyes['surprise'], EYES)
            # self.play_hold(self.face.hold_surprise, EYES)
            # self.play_seq(reversed(self.face.eyes['surprise']), EYES)

            # # off
            # self.play_seq(self.face.eyes['off'], EYES)
            # self.play_seq(reversed(self.face.eyes['off']), EYES)

            # # heart in to loop
            # self.play_seq(self.face.eyes['off'], EYES)
            # self.play_seq(self.face.eyes['heart_in'], EYES)
            # self.play_seq(self.face.eyes['heart_loop'], EYES)
            # self.play_seq(self.face.eyes['heart_loop'], EYES)
            # self.play_seq(self.face.eyes['heart_loop'], EYES)
            # self.play_seq(reversed(self.face.eyes['heart_in']), EYES)
            # self.play_seq(reversed(self.face.eyes['off']), EYES)

            # # sunglasses
            # self.play_seq(self.face.eyes['sunglasses'], EYES)
            # self.play_hold(self.face.hold_sunglasses, EYES)
            # self.play_seq(reversed(self.face.eyes['sunglasses']), EYES)

            # # x eyes
            # self.play_seq(self.face.eyes['x_eyes'], EYES)
            # self.play_hold(self.face.hold_x_eyes, EYES)
            # self.play_seq(reversed(self.face.eyes['x_eyes']), EYES)

            # # left
            # self.play_seq(self.face.eyes['left'], EYES)
            # self.play_hold(self.face.hold_left, EYES)
            # self.play_seq(reversed(self.face.eyes['left']), EYES)

            # # right
            # self.play_seq(self.face.eyes['right'], EYES)
            # self.play_hold(self.face.hold_right, EYES)
            # self.play_seq(reversed(self.face.eyes['right']), EYES)

            # # ! !
            # self.play_seq(self.face.eyes['exclaim'], EYES)
            # self.play_hold(self.face.hold_exclaim, EYES)
            # self.play_seq(reversed(self.face.eyes['exclaim']), EYES)

            # # ? ?
            # self.play_seq(self.face.eyes['question'], EYES)
            # self.play_hold(self.face.hold_question, EYES)
            # self.play_seq(reversed(self.face.eyes['question']), EYES)

            # ##### MOUTH #####
            # # idle
            # self.play_hold(self.face.hold_line, MOUTH)

            # # smile closed
            # self.play_seq(self.face.mouths['smile_closed'], MOUTH)
            # self.play_hold(self.face.hold_smile_closed, MOUTH)
            # self.play_seq(reversed(self.face.mouths['smile_closed']), MOUTH)

            # # smile open
            # self.play_seq(self.face.mouths['smile_open'], MOUTH)
            # self.play_hold(self.face.hold_smile_open, MOUTH)
            # self.play_seq(reversed(self.face.mouths['smile_open']), MOUTH)

            # # frown closed
            # self.play_seq(self.face.mouths['frown_closed'], MOUTH)
            # self.play_hold(self.face.hold_frown_closed, MOUTH)
            # self.play_seq(reversed(self.face.mouths['frown_closed']), MOUTH)

            # # frown open
            # self.play_seq(self.face.mouths['frown_open'], MOUTH)
            # self.play_hold(self.face.hold_frown_open, MOUTH)
            # self.play_seq(reversed(self.face.mouths['frown_open']), MOUTH)
            
            # # surprise o
            # self.play_seq(self.face.mouths['o_mouth'], MOUTH)
            # self.play_hold(self.face.hold_o_mouth, MOUTH)
            # self.play_seq(reversed(self.face.mouths['o_mouth']), MOUTH)

            # # smirk
            # self.play_seq(self.face.mouths['smirk'], MOUTH)
            # self.play_hold(self.face.hold_smirk, MOUTH)
            # self.play_seq(reversed(self.face.mouths['smirk']), MOUTH)            

            # # tongue out
            # self.play_seq(self.face.mouths['tongue'], MOUTH)
            # self.play_hold(self.face.hold_tongue, MOUTH)
            # self.play_seq(reversed(self.face.mouths['tongue']), MOUTH)

            # # cat
            # self.play_seq(self.face.mouths['cat'], MOUTH)
            # self.play_hold(self.face.hold_cat, MOUTH)
            # self.play_seq(reversed(self.face.mouths['cat']), MOUTH)

            # # off
            # self.play_seq(self.face.mouths['mouth_off'], MOUTH)
            # self.play_hold(self.face.hold_mouth_off, MOUTH)
            # self.play_seq(reversed(self.face.mouths['mouth_off']), MOUTH)
