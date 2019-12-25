#!/usr/bin/env python

# Face.py for loading GIFs and images
import os
from PIL import Image

from animation import Animation

class Face:

    def __init__(self):
        self.eyes = {}
        self.mouths = {}
        self.hold_overrides = {'blink' : 0, 'smile_closed' : 0}
        self.hold_frames = {}
        self.eye_latches = {'blink'}
        self.mouth_latches = {'smile_closed'}

        for item in os.listdir("faces/eyes"):
            filename = item.split(".gif")[0]
            self.eyes[filename] = self.gif_loader("faces/eyes/" + item, filename)

        for item in os.listdir("faces/mouths"):
            filename = item.split(".gif")[0]
            self.mouths[filename] = self.gif_loader("faces/mouths/" + item, filename)
        
        for i,value in self.mouths.items():
            self.hold_frames[i] = value[self.hold_overrides[i]] if self.hold_overrides.get(i, None) else value[-1]
        for i,value in self.eyes.items():
            self.hold_frames[i] = value[self.hold_overrides[i]] if self.hold_overrides.get(i, None) else value[-1]
        #print(self.hold_frames)
        self.parsed_latches = {}
        for item in self.eye_latches:           
            eye = self.eyes[item]
            self.parsed_latches[eye] = item

        for item in self.mouth_latches:
            mouth = self.mouths[item]
            self.parsed_latches[mouth] = item
        
    
    def is_latch(self, expression):
        return expression in self.parsed_latches

    def gif_loader(self, file, filename):
        # loads a gif into the array for storage
        arr = []
        gif = Image.open(file, 'r')
        try:
            while(True):
                arr.append(gif.copy().convert('RGB'))
                gif.seek(len(arr))
        except EOFError:
            return Animation(filename, arr)