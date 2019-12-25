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
from animation import Animation

# constants used throughout project
WIDTH = 32
HEIGHT = 32
SPEED = 1.0 / 15.0
IDLE_TIME = 50
EYES = 0
MOUTHS = 16


class Kabuki:

    def __init__(self, matrix):
        self.matrix = matrix
        self.face = Face()
        self.eye_queue = queue.Queue()
        self.mouth_queue = queue.Queue()
        self.loop_proc = Process(target=self.loop)
        self.eye_latch = self.face.hold_frames['blink']
        self.mouth_latch = self.face.hold_frames['smile_closed']

        # flask listener is a seperate thread
        t = threading.Thread(target=self.loop)
        t.start()
        
        # start the render loop on main thread
        self.render_loop()

    def start_flask(self):
        self.loop_proc.start()

    def play_seq(self, expression, board, direction):
        #add sequence to correct queue and reverse if needed
        if board == EYES:
            sequence = self.face.eyes[expression]
        else:
            sequence = self.face.mouths[expression]
      
        if direction == 'r':
            sequence = sequence.get_reversed()

        if board == EYES:
            self.eye_queue.put(sequence)
        else:
            self.mouth_queue.put(sequence)

    def play_hold(self, hold, board, duration=IDLE_TIME):
        #generate a bunch of frames to hold
        hold_seq = Animation('hold_' + hold, [self.face.hold_frames[hold] for i in range(duration)])

        if board == EYES:
            self.eye_queue.put(hold_seq)
        else:
            self.mouth_queue.put(hold_seq)

    def compute_eyes(self):
        idx = 0
        #default hold is no expression from blink
        idle_eye_seq = Animation('idle', [self.face.hold_frames['blink']])
        current_eye = idle_eye_seq
        while(True):
            if self.eye_queue.empty() and len(current_eye) == idx:
                #reset
                idx = 0
                current_eye = idle_eye_seq
            else:
                if not self.eye_queue.empty():
                    current_eye = self.eye_queue.get()
                    if self.face.is_latch(current_eye):
                        idle_eye_seq = current_eye
                    idx = 0
            #print(current_eye, idx)
            yield current_eye[idx]
            idx += 1

    def compute_mouth(self):
        idx = 0
        #default hold is a line from smile_closed
        idle_mouth_seq = Animation('idle_mouth', [self.face.hold_frames['smile_closed']])
        current_mouth = idle_mouth_seq
        while(True):
            if self.mouth_queue.empty() and len(current_mouth) == idx:
                #reset
                idx = 0
                current_mouth = idle_mouth_seq
            else:
                if not self.mouth_queue.empty():
                    current_mouth = self.mouth_queue.get()
                    if self.face.is_latch(current_mouth):
                        idle_mouth_seq = current_mouth
                    idx = 0
            yield current_mouth[idx]
            idx += 1

    def compute_frame(self):
        eye_frame = self.compute_eyes()
        mouth_frame = self.compute_mouth()
        
        while(True):
            # do work to combine eyes and mouths and yield resulting frame
            frame = Image.new('RGB', (WIDTH, HEIGHT))
            try:
                frame.paste(next(eye_frame), (0, EYES))
            except Exception as e:
                print('Eye Exception:', e)
            
            try:
                frame.paste(next(mouth_frame), (0, MOUTHS))
            except Exception as e:
                print('Mouth Exception:', e)
            yield frame
            

    def render_loop(self):
        next_frame = self.compute_frame()
        while(True):
            try:
                self.matrix.SetImage(next(next_frame), 0, 0)
                time.sleep(SPEED)
            except Exception as e:
                print('Render Exception:', e)

    def loop(self):
        while(True):
            self.play_seq('blink', EYES, 'f')
            time.sleep(2)
            self.play_seq('happy', EYES, 'f')
            time.sleep(2)
            self.play_hold('happy', EYES, 200)
            time.sleep(2)
            self.play_seq('happy', EYES, 'r')
            time.sleep(3)
            self.play_seq('smile_closed', MOUTHS, 'f')
            time.sleep(2)
            self.play_hold('smile_closed', MOUTHS)
            time.sleep(2)
            self.play_seq('smile_closed', MOUTHS, 'r')

            time.sleep(3)
            self.play_seq('sad', EYES, 'f')
            time.sleep(2)
            self.play_hold('sad', EYES)
            time.sleep(2)
            self.play_seq('frown_open', MOUTHS, 'f')
            time.sleep(2)
            self.play_hold('frown_open', MOUTHS, 200)
            time.sleep(2)
            self.play_seq('cry', EYES, 'f')
            time.sleep(1)
            self.play_seq('cry', EYES, 'f')
            time.sleep(1)
            self.play_seq('cry', EYES, 'f')
            time.sleep(1)
            self.play_seq('sad', EYES, 'r')
            time.sleep(2)
            self.play_seq('frown_open', MOUTHS, 'r')
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

            # ##### mouths #####
            # # idle
            # self.play_hold(self.face.hold_line, mouths)

            # # smile closed
            # self.play_seq(self.face.mouths['smile_closed'], mouths)
            # self.play_hold(self.face.hold_smile_closed, mouths)
            # self.play_seq(reversed(self.face.mouths['smile_closed']), mouths)

            # # smile open
            # self.play_seq(self.face.mouths['smile_open'], mouths)
            # self.play_hold(self.face.hold_smile_open, mouths)
            # self.play_seq(reversed(self.face.mouths['smile_open']), mouths)

            # # frown closed
            # self.play_seq(self.face.mouths['frown_closed'], mouths)
            # self.play_hold(self.face.hold_frown_closed, mouths)
            # self.play_seq(reversed(self.face.mouths['frown_closed']), mouths)

            # # frown open
            # self.play_seq(self.face.mouths['frown_open'], mouths)
            # self.play_hold(self.face.hold_frown_open, mouths)
            # self.play_seq(reversed(self.face.mouths['frown_open']), mouths)
            
            # # surprise o
            # self.play_seq(self.face.mouths['o_mouth'], mouths)
            # self.play_hold(self.face.hold_o_mouth, mouths)
            # self.play_seq(reversed(self.face.mouths['o_mouth']), mouths)

            # # smirk
            # self.play_seq(self.face.mouths['smirk'], mouths)
            # self.play_hold(self.face.hold_smirk, mouths)
            # self.play_seq(reversed(self.face.mouths['smirk']), mouths)            

            # # tongue out
            # self.play_seq(self.face.mouths['tongue'], mouths)
            # self.play_hold(self.face.hold_tongue, mouths)
            # self.play_seq(reversed(self.face.mouths['tongue']), mouths)

            # # cat
            # self.play_seq(self.face.mouths['cat'], mouths)
            # self.play_hold(self.face.hold_cat, mouths)
            # self.play_seq(reversed(self.face.mouths['cat']), mouths)

            # # off
            # self.play_seq(self.face.mouths['mouth_off'], mouths)
            # self.play_hold(self.face.hold_mouth_off, mouths)
            # self.play_seq(reversed(self.face.mouths['mouth_off']), mouths)
