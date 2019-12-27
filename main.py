#!/usr/bin/env python

# Main python

# imports - use the rpi-rgb-led-matrix instructions to install dependencies
import time
import threading
from flask import Flask
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from kabuki import Kabuki

ROWS = 16
COLS = 32

if __name__ == "__main__":
    # Configuration for the matrix, adafruit hat in a U configuration, 2 chain
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 2
    options.pixel_mapper_config = "U-mapper"
    options.gpio_slowdown = 4
    options.hardware_mapping = "adafruit-hat"
    options.drop_privileges = 0
    print(
        "Starting Kabuki with",
        str(options.rows),
        "rows",
        str(options.cols),
        "cols",
        str(options.pixel_mapper_config),
        str(options.hardware_mapping),
    )
    matrix = RGBMatrix(options=options)

    try:
        kabuki = Kabuki(matrix)
    except KeyboardInterrupt:
        matrix.Clear()
        print("Ctrl+C pressed, exiting")
        raise
    except Exception as e:
        print("Exception: ", e)
