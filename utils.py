#!/usr/bin/env python
import os
import re
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


def get_host_ip():
    return re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), os.popen('ip addr show usb0').read()).groups()[0]


def command_shutdown():
    print('Shutdown commanded')
    os.system('sudo shutdown -h 00:10 &')


def command_shutdown_cancel():
    print('Shutdown canceled')
    os.system('sudo shutdown -c &')


def command_restart():
    print('Restart commanded')
    os.system('sudo shutdown -r &')
