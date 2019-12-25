#!/usr/bin/env python

# Main python

# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from kabuki import Kabuki

ROWS = 16
COLS = 32

if __name__ == '__main__':
    # Configuration for the matrix, adafruit hat in a U configuration, 2 chain
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 2
    options.pixel_mapper_config = 'U-mapper'
    options.gpio_slowdown = 4
    options.hardware_mapping = 'adafruit-hat'
    print('Starting Kabuki with', str(options.rows), 'rows', str(options.cols), 'cols', str(options.pixel_mapper_config), str(options.hardware_mapping))
    matrix = RGBMatrix(options = options)

    kabuki = Kabuki(matrix)
    kabuki.start_render()

