# Kabuki

Code repository for the Kabuki helmet project.

## Pre-requisites

- RPi 3 and up
- Python3 (may be installed by script)
- `build-essential` (may be installed by script)
- Two 16x32 LED matricies (ours are from Adafruit)
- Clone and install ~~<https://github.com/hzeller/rpi-rgb-led-matrix>~~
  - [use Adafruit's script to bootstrap library instead of attempting to build yourself](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices#step-6-log-into-your-pi-to-install-and-run-software-1745233)
  - Follow instructions to install Python libraries
- Flask (pip install flask)

## Running

Either run `./start.sh` or `python3 main.py`

## Set up specific values

- rows: 16
- cols: 32
- chain_length = 2
- pixel_mapper_config = "U-mapper"
- hardware_mapping = "adafruit-hat"
