#!/usr/bin/env python

# Face.py for loading GIFs and images
import os
from PIL import Image

# loads a gif into the array for storage
def gif_loader(file):
    arr = []
    gif = Image.open(file, 'r')
    try:
        while(True):
            arr.append(gif.copy().convert('RGB'))
            gif.seek(len(arr))
    except EOFError:
        return arr

class Face:

    def __init__(self):

        self.eyes = {}
        self.mouths = {}
        self.hold_overrides = {'blink' : 0, 'smile_closed' : 0}
        self.hold_frames = {}


        for item in os.listdir("faces/eyes"):
            filename = item.split(".gif")[0]
            self.eyes[filename] = gif_loader("faces/eyes/" + item)

        for item in os.listdir("faces/mouths"):
            filename = item.split(".gif")[0]
            self.mouths[filename] = gif_loader("faces/mouths/" + item)
        
        for i,value in self.mouths.items():
            self.hold_frames[i] = value[self.hold_overrides[i]] if self.hold_overrides.get(i, None) else value[-1]
        for i,value in self.eyes.items():
            self.hold_frames[i] = value[self.hold_overrides[i]] if self.hold_overrides.get(i, None) else value[-1]
        #print(self.hold_frames)