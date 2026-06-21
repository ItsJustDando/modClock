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

After entering the env using `source env/bin/activate`
If you downloaded the dependencies correctly through the setup instructions, you can **skip this part** and go to wiring.
- For the 7-segment LED: [Adafruit HT16K33 Python module info](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33)
- To control GPIO pins, use `gpiozero` which should be installed onto the Raspberry Pi OS image by default.\

  Just in case, you should use:
  ```bash
  pip install gpiozero
  ```
  
  If needed, a pin library:
  ```bash
  pip install RPi.GPIO
  ```
- To play the alarm ring sound, the `playsound3` module is used:
  ```bash
  pip install playsound3
  ```

All required dependencies can also be found in the `requirements.txt` file

## Automatic Start-up

### 1. Create `.service` file
To allow the Pi to start modClock automatically on boot, you should use systemd. It will run the `.service` file on start-up.
To make a this service, call it let's say `modClock.service` (you can change this name of course), input the following into the console:
```bash
sudo nano /usr/lib/systemd/system/modClock.service
```
Write the following in the service file:
```nano
[Unit]
Description=modClock
After=network-online.target time-sync.target sound.target
Wants=network-online.target

[Service]
User=(your username)
Group=(your username)
SupplementaryGroups=audio
WorkingDirectory=(path to code file - without .py)
ExecStart=(path to env python file) -u code.py
ExecStartPre=/bin/sleep 5
Environment=XDG_RUNTIME_DIR=/run/user/1000

[Install]
WantedBy=multi-user.target
```
Replace all "( )" sections with the requested part.
Press `Ctrl + X` then `Y` then `Enter` to exit, save and close the service.

### 2. Activate `.service` file
Now that the service is create, you have to activate the file. To do so, input the following into the command line:
```bash
sudo systemctl activate /usr/lib/systemd/system/modClock.service
```
And you're done! When you power on the Pi, the modClock will turn on and everything will run.

If it does not run, check the error using
```bash
sudo systemctl status /usr/lib/systemd/system/modClock.service
```
