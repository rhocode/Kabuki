#!/usr/bin/env python

# Main python

# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import time
import threading
from threading import queue
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from kabuki import Kabuki

if __name__ == '__main__':
	# Configuration for the matrix, adafruit hat in a U configuration, 2 chain
	options = RGBMatrixOptions()
	options.rows = ROWS
	options.cols = COLS
	options.chain_length = 2
	options.pixel_mapper_config = 'U-mapper'
	options.gpio_slowdown = 4
	options.hardware_mapping = 'adafruit-hat'

	matrix = RGBMatrix(options = options)

	kabuki = Kabuki(matrix)
	kabuki.loop()

