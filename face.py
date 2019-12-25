#!/usr/bin/env python

# Face.py for loading GIFs and images
from PIL import Image

# loads a gif into the array for storage
def gif_loader(file):
	arr = []
	gif = Image.open(file, 'r')
	try:
		while 1:
			arr.append(gif.copy().convert('RGB'))
			gif.seek(len(arr))
	except EOFError:
		return arr

class Face:

	def __init__(self):
		self.anim_blink = gif_loader('faces/blink.gif')
		self.anim_happy = gif_loader('faces/happy.gif')
		self.anim_sad = gif_loader('faces/sad.gif')
		self.anim_cry = gif_loader('faces/cry.gif')
		self.anim_angry = gif_loader('faces/angry.gif')
		self.anim_suspicious = gif_loader('faces/suspicious.gif')
		self.anim_sleep = gif_loader('faces/sleep.gif')
		self.anim_surprise = gif_loader('faces/surprise.gif')
		self.anim_off = gif_loader('faces/off.gif')
		self.anim_heart_in = gif_loader('faces/heart_in.gif')
		self.anim_heart_loop = gif_loader('faces/heart_loop.gif')
		self.anim_sunglasses = gif_loader('faces/sunglasses.gif')
		self.anim_x_eyes = gif_loader('faces/x_eyes.gif')
		self.anim_left = gif_loader('faces/left.gif')
		self.anim_right = gif_loader('faces/right.gif')
		self.anim_exclaim = gif_loader('faces/exclaim.gif')
		self.anim_question = gif_loader('faces/question.gif')
		self.anim_thinking = gif_loader('faces/thinking.gif')
		self.anim_smile_closed = gif_loader('faces/smile_closed.gif')
		self.anim_smile_open = gif_loader('faces/smile_open.gif')
		self.anim_frown_closed = gif_loader('faces/frown_closed.gif')
		self.anim_frown_open = gif_loader('faces/frown_open.gif')
		self.anim_o = gif_loader('faces/o_mouth.gif')
		self.anim_smirk = gif_loader('faces/smirk.gif')
		self.anim_tongue = gif_loader('faces/tongue.gif')
		self.anim_cat = gif_loader('faces/cat.gif')
		self.anim_mouth_off = gif_loader('faces/mouth_off.gif')
		

		self.hold_idle = self.anim_blink[0]
		self.hold_happy = self.anim_happy[-1]
		self.hold_sad = self.anim_sad[-1]
		self.hold_angry = self.anim_angry[-1]
		self.hold_suspicious = self.anim_suspicious[-1]
		self.hold_sleep = self.anim_sleep[-1]
		self.hold_surprise = self.anim_surprise[-1]
		self.hold_off = self.anim_off[-1]
		self.hold_sunglasses = self.anim_sunglasses[-1]
		self.hold_x_eyes = self.anim_x_eyes[-1]
		self.hold_left = self.anim_left[-1]
		self.hold_right = self.anim_right[-1]
		self.hold_exclaim = self.anim_exclaim[-1]
		self.hold_question = self.anim_question[-1]
		self.hold_thinking = self.anim_thinking[-1]
		self.hold_line = self.anim_smile_closed[0]
		self.hold_smile_closed = self.anim_smile_closed[-1]
		self.hold_smile_open = self.anim_smile_open[-1]
		self.hold_frown_closed = self.anim_frown_closed[-1]
		self.hold_frown_open = self.anim_frown_open[-1]
		self.hold_o_mouth = self.anim_o[-1]
		self.hold_smirk = self.anim_smirk[-1]
		self.hold_tongue = self.anim_tongue[-1]
		self.hold_cat = self.anim_cat[-1]
		self.hold_mouth_off = self.anim_mouth_off[-1]