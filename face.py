#!/usr/bin/env python

# Face.py for loading GIFs and images
import utils
from animation import Animation

class Face:

    def __init__(self):
        self.eyes = {}
        self.mouths = {}
        self.hold_overrides = {'blink' : 0, 'idle_mouth' : 0}
        self.hold_frames = {}
        self.eye_latches = {'blink'}
        self.mouth_latches = {'smile_closed'}
        self.special_attr_eyes = {
            'blink' : {
                'hold_frame' : 0,
            },
        }
        self.special_attr_mouths = {
            'idle_mouth' : {
                'hold_frame' : 0,
            },
        }

                # Load Eyes
        utils.load_files("faces/eyes", self.special_attr_eyes, self.eyes, "faces/eyes/")
        
        # Load Mouths
        utils.load_files("faces/mouths", self.special_attr_mouths, self.mouths, "faces/mouths/")
        
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
        
    
    def is_latch(self, animation):
        return animation.is_latch()