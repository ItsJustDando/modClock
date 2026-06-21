# modClock
Alarm clock that is controlled and run on a Raspberry Pi Zero W.

## Parts
Format below is as follows: `[part amount] part name`
- [1] Raspberry Pi Zero W
- [1] Adafruit 0.56" 7-segment LED HT16K33 Backpack
- [2] 220 Ohm resistors
- [2] LEDs
- [3] Push Button Switch 4 pin

## Dependencies
On the Raspberry Pi Zero W, you will need to create a Virtual Environment to install modules for your project.
Full documentation in the `env_setup.md` file

If you downloaded the dependencies correctly through the setup instructions, you can skip this part and go to wiring.
- For the 7-segment LED: [Adafruit HT16K33 Python module info](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33)
- To control GPIO pins, use `gpiozero` which should be installed onto the Raspberry Pi OS image by default.\
  Just in case, you should use: `pip install gpiozero`\
  If needed, a pin library: `pip install RPi.GPIO`
- To play the alarm ring sound, the `playsound3` module is used:
  `pip install playsound3`

All required dependencies can also be found in the `requirements.txt` file
