#!/usr/bin/env python
import os
from PIL import Image

from animation import Animation
# utils.py for misc utils

def load_files(used_dir, overrides, dest_dict, path):
    for item in os.listdir(used_dir):
        filename = item.split(".gif")[0]
        attrs = overrides.get(filename, {})
        dest_dict[filename] = gif_loader(path + item, filename, attrs)

def gif_loader(file, filename, attrs):
    # loads a gif into the array for storage
    arr = []
    gif = Image.open(file, 'r')
    try:
        while(True):
            arr.append(gif.copy().convert('RGB'))
            gif.seek(len(arr))
    except EOFError:
        return Animation(filename, arr, attrs)