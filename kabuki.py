#!/usr/bin/env python

# Main kabuki.py

# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import time
import queue
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
		self.eye_queue = JoinableQueue()
		self.mouth_queue = JoinableQueue()
		self.render_queue = JoinableQueue()
		self.loop_proc = Process(target=self.loop)
		self.compute_proc = Process(target=self.compute_frame)
		self.render_proc = Process(target=self.render_loop)
		self.reset_face()

	def start_render(self):
		self.loop_proc.start()
		#self.loop_proc.join()
		self.compute_proc.start()
		self.render_proc.start()
		#self.compute_proc.join()
		#self.render_proc.join()

	def play_seq(self, sequence, board):
		for frame in sequence:
			#self.matrix.SetImage(frame, 0, board)
			if board == EYES:
				self.eye_queue.put(frame)
			else:
				self.mouth_queue.put(frame)
			#time.sleep(SPEED)

	def play_hold(self, hold, board):
		for frame in range(0, IDLE_TIME):
			#self.matrix.SetImage(hold, 0, board)
			if board == EYES:
				self.eye_queue.put(frame)
			else:
				self.mouth_queue.put(frame)
			#time.sleep(SPEED)

	def compute_frame(self):
		while 1:
			# do work to combine eye and mouth and add to render queue
			self.eye_queue.join()
			self.mouth_queue.join()
			if self.eye_queue.empty():
				self.play_hold(self.face.hold_idle, EYES)
			if self.mouth_queue.empty():
				self.play_hold(self.face.hold_line, MOUTH)

			frame = Image.new('RGB', (WIDTH, HEIGHT))
			frame.paste(self.eye_queue.get(), 0, EYES)
			frame.paste(self.mouth_queue.get(), 0, MOUTH)
			self.render_queue.put(frame)

	def render_loop(self):
		print('render start')
		while 1:
			self.render_queue.join()
			while not self.render_queue.empty():
				#self.compute_frame()
				self.matrix.SetImage(self.render_queue.get(), 0, 0)
				time.sleep(SPEED)
		print('render end')

	def reset_face(self):
		self.play_hold(self.face.hold_idle, EYES)
		self.play_seq(self.face.anim_blink, EYES)
		self.play_hold(self.face.hold_idle, EYES)
		self.play_hold(self.face.hold_line, MOUTH)

	def loop(self):
		print('start')
		#while 1:
		#self.matrix.Clear()
		# animations with "loop" are standalone loops, but may need to be prefaced
		# by a different state (eg sad first then cry) - if triggered seperately, split out seq
		# unless noted, faces return to neutral

		###### EYES #######
		# idle (blink) loop
		self.play_hold(self.face.hold_idle, EYES)
		self.play_seq(self.face.anim_blink, EYES)
		self.play_hold(self.face.hold_idle, EYES)
		
		# happy
		self.play_seq(self.face.anim_happy, EYES)
		self.play_hold(self.face.hold_happy, EYES)
		self.play_seq(reversed(self.face.anim_happy), EYES)
		
		# sad
		self.play_seq(self.face.anim_sad, EYES)
		self.play_hold(self.face.hold_sad, EYES)
		self.play_seq(reversed(self.face.anim_sad), EYES)
		
		# cry loop (return to sad)
		self.play_seq(self.face.anim_sad, EYES)
		self.play_seq(self.face.anim_cry, EYES)
		self.play_seq(self.face.anim_cry, EYES)
		self.play_seq(self.face.anim_cry, EYES)
		self.play_seq(reversed(self.face.anim_sad), EYES)
		
		# angry
		self.play_seq(self.face.anim_angry, EYES)
		self.play_hold(self.face.hold_angry, EYES)
		self.play_seq(reversed(self.face.anim_angry), EYES)

		# suspicious
		self.play_seq(self.face.anim_suspicious, EYES)
		self.play_hold(self.face.hold_suspicious, EYES)
		self.play_seq(reversed(self.face.anim_suspicious), EYES)

		# sleep
		self.play_seq(self.face.anim_sleep, EYES)
		self.play_hold(self.face.hold_sleep, EYES)
		self.play_seq(reversed(self.face.anim_sleep), EYES)

		# surprise
		self.play_seq(self.face.anim_surprise, EYES)
		self.play_hold(self.face.hold_surprise, EYES)
		self.play_seq(reversed(self.face.anim_surprise), EYES)

		# off
		self.play_seq(self.face.anim_off, EYES)
		self.play_seq(reversed(self.face.anim_off), EYES)

		# heart in to loop
		self.play_seq(self.face.anim_off, EYES)
		self.play_seq(self.face.anim_heart_in, EYES)
		self.play_seq(self.face.anim_heart_loop, EYES)
		self.play_seq(self.face.anim_heart_loop, EYES)
		self.play_seq(self.face.anim_heart_loop, EYES)
		self.play_seq(reversed(self.face.anim_heart_in), EYES)
		self.play_seq(reversed(self.face.anim_off), EYES)

		# sunglasses
		self.play_seq(self.face.anim_sunglasses, EYES)
		self.play_hold(self.face.hold_sunglasses, EYES)
		self.play_seq(reversed(self.face.anim_sunglasses), EYES)

		# x eyes
		self.play_seq(self.face.anim_x_eyes, EYES)
		self.play_hold(self.face.hold_x_eyes, EYES)
		self.play_seq(reversed(self.face.anim_x_eyes), EYES)

		# left
		self.play_seq(self.face.anim_left, EYES)
		self.play_hold(self.face.hold_left, EYES)
		self.play_seq(reversed(self.face.anim_left), EYES)

		# right
		self.play_seq(self.face.anim_right, EYES)
		self.play_hold(self.face.hold_right, EYES)
		self.play_seq(reversed(self.face.anim_right), EYES)

		# ! !
		self.play_seq(self.face.anim_exclaim, EYES)
		self.play_hold(self.face.hold_exclaim, EYES)
		self.play_seq(reversed(self.face.anim_exclaim), EYES)

		# ? ?
		self.play_seq(self.face.anim_question, EYES)
		self.play_hold(self.face.hold_question, EYES)
		self.play_seq(reversed(self.face.anim_question), EYES)

		##### MOUTH #####
		# idle
		self.play_hold(self.face.hold_line, MOUTH)

		# smile closed
		self.play_seq(self.face.anim_smile_closed, MOUTH)
		self.play_hold(self.face.hold_smile_closed, MOUTH)
		self.play_seq(reversed(self.face.anim_smile_closed), MOUTH)

		# smile open
		self.play_seq(self.face.anim_smile_open, MOUTH)
		self.play_hold(self.face.hold_smile_open, MOUTH)
		self.play_seq(reversed(self.face.anim_smile_open), MOUTH)

		# frown closed
		self.play_seq(self.face.anim_frown_closed, MOUTH)
		self.play_hold(self.face.hold_frown_closed, MOUTH)
		self.play_seq(reversed(self.face.anim_frown_closed), MOUTH)

		# frown open
		self.play_seq(self.face.anim_frown_open, MOUTH)
		self.play_hold(self.face.hold_frown_open, MOUTH)
		self.play_seq(reversed(self.face.anim_frown_open), MOUTH)
		
		# surprise o
		self.play_seq(self.face.anim_o, MOUTH)
		self.play_hold(self.face.hold_o_mouth, MOUTH)
		self.play_seq(reversed(self.face.anim_o), MOUTH)

		# smirk
		self.play_seq(self.face.anim_smirk, MOUTH)
		self.play_hold(self.face.hold_smirk, MOUTH)
		self.play_seq(reversed(self.face.anim_smirk), MOUTH)			

		# tongue out
		self.play_seq(self.face.anim_tongue, MOUTH)
		self.play_hold(self.face.hold_tongue, MOUTH)
		self.play_seq(reversed(self.face.anim_tongue), MOUTH)

		# cat
		self.play_seq(self.face.anim_cat, MOUTH)
		self.play_hold(self.face.hold_cat, MOUTH)
		self.play_seq(reversed(self.face.anim_cat), MOUTH)

		# off
		self.play_seq(self.face.anim_mouth_off, MOUTH)
		self.play_hold(self.face.hold_mouth_off, MOUTH)
		self.play_seq(reversed(self.face.anim_mouth_off), MOUTH)
		print('end')