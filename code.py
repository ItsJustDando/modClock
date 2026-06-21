import time
import math

import board
import threading
import signal
from playsound3 import playsound
from gpiozero import Button, LED
from adafruit_ht16k33 import segments



### DECLARING PARTS

# time
hour = 0
minute = 0
second = 0

# 7bit display
i2c = board.I2C()
display = segments.Seg7x4(i2c)
brightness_level = 0
brightness_rate = 0.135
brightness_screen_time_left = 0

#leds
ledPM = LED(27)
ledAlarm = LED(22)

# buttons
btn1 = Button(4)
btn2 = Button(17)
btn3 = Button(23)
btn_cooldown = [0, 0, 0]
btn_cooldown_press = 1  # cooldown time for button press in seconds
btn_cooldown_hold = 3  # cooldown time for button hold in seconds

is_meridian_time = False

alarm_mode_active = False
alarm_ringing = False
alarm_activated = False
alarm_turned_off = False

alarm_sounds = [#  add file names to this array to have access to them
    'spooky_organ.mp3',
    'digital_alarm_beep.mp3'
]
alarm_sound_index = 0  # modify this index to change the default sound
alarm_sound_path = 'resources/'+alarm_sounds[alarm_sound_index]
alarm_sound = playsound(alarm_sound_path, False)
alarm_sound.stop()

alarm_time = {
    'hour' : 6,
    'minute' : 0
}



### FUNCTIONS

def update_display():
    global display, ledPM, is_meridian_time, hour, minute, second

    hourStr, minuteStr = str(hour), str(minute)

    ledPM.off()
    if (alarm_mode_active):
        hourStr = str(alarm_time['hour'])
        minuteStr = str(alarm_time['minute'])
    else:
        if ((hour > 12) and (is_meridian_time)):
            ledPM.on()
            hourStr = str(int(hourStr) - 12)

    hourStr = '0' + hourStr
    if (len(minuteStr) == 1): minuteStr = '0' + minuteStr
    
    display.print(hourStr + minuteStr)
    display.colon = bool((second % 2) or (alarm_mode_active))
    print('display updated successfully')

def update_time():  
    global hour, minute, second, alarm_turned_off
    #print('updating time variables')

    timeStamp = time.localtime()
    hour = timeStamp.tm_hour
    minute = timeStamp.tm_min
    second = timeStamp.tm_sec

    print('time variables updated to: ', hour, ":", minute, ":", second)

    if (alarm_activated):
        if ((not alarm_mode_active) and (not alarm_ringing)):
            if ((alarm_time['hour'] == hour) and (alarm_time['minute'] == minute)):
                if (not alarm_turned_off):
                    print('time variables are equal to alarm time variables: [hour=', hour, '/alarmHour=', alarm_time['hour'], '] [minute=',minute,'/alarmMinute=',alarm_time['minute'],']')
                    alarm_ring()
            else:
                if (alarm_turned_off): alarm_turned_off = False
                print('alarm turned off variable set back to: false')

def display_show_brightness():
    global display, brightness_screen_time_left

    #                       bottomleft--, ,--bottomright
    #                         middle--v v v v--top
    # display.set_digit_raw(index, 0b00000000)
    #                       decimal--^ ^ ^ ^--topright
    #                         topleft--' '--bottom

    brightness_screen_time_left = 2

    display.colon = False
    display.fill(False)
    current_brightness = display.brightness
    brightness_bits = [0b00000000, 0b00000000, 0b00000000, 0b00000000]
    
    if (current_brightness > 0):
        brightness_bits[0] = brightness_bits[0] | (1 << 4)
        brightness_bits[0] = brightness_bits[0] | (1 << 5)
    
    if (current_brightness > brightness_rate*1):
        brightness_bits[0] = brightness_bits[0] | (1 << 2)
        brightness_bits[0] = brightness_bits[0] | (1 << 1)

    for factor in range(8):
        segment_to_activate = [5, 4]
        if (factor % 2 == 1): segment_to_activate = [2, 1]

        digit_to_change = math.floor(factor / 2)

        if (current_brightness > brightness_rate*factor):
            brightness_bits[digit_to_change] = brightness_bits[digit_to_change] | (1 << segment_to_activate[0])
            brightness_bits[digit_to_change] = brightness_bits[digit_to_change] | (1 << segment_to_activate[1])

    for i in range(len(brightness_bits)):
        display.set_digit_raw(i, brightness_bits[i])

def toggle_meridian_time():
    global is_meridian_time
    is_meridian_time = not is_meridian_time
    print('meridian time set to: ', ['false', 'true'][is_meridian_time])

# ALARM FUNCTIONS
def alarm_play_sound():
    global alarm_sound
    alarm_sound.stop()
    alarm_sound = playsound(alarm_sound_path, False)
    print('playing alarm sound: ', alarm_sounds[alarm_sound_index])

def alarm_set_sound(index: int):
    global alarm_sound_path, alarm_sound_index
    alarm_sound_index = index
    alarm_sound_path = 'resources/'+alarm_sounds[index]
    print('alarm sound set to: ', alarm_sounds[index])

def alarm_ring():
    global alarm_ringing, ledAlarm

    alarm_ringing = True
    ledAlarm.blink()
    alarm_play_sound()
    print('alarm ring turned on')

def alarm_ring_off():
    global alarm_ringing, ledAlarm, alarm_sound, alarm_turned_off

    alarm_ringing = False
    alarm_turned_off = True
    ledAlarm.off()
    alarm_sound.stop()
    print('alarm ring turned off')

def alarm_mode(state : bool):
    global alarm_mode_active
    alarm_mode_active = state
    
    print('alarm mode [',state,']')

# BUTTON ACTIONS
def btn1_action():
    global alarm_time, display

    print('--- btn1 released ---')
    if (btn_cooldown[0] > 0): 
        print('btn1 cooldown at ', btn_cooldown[0], ', leaving action')
        return

    if (alarm_mode_active):
        alarm_time['hour'] = alarm_time['hour'] + 1
        if (alarm_time['hour'] > 24): alarm_time['hour'] = 1
        print('btn1 > alarm time hour increased to: ', alarm_time['hour'])
    else:
        toggle_meridian_time()

    
    update_display()
    btn_cooldown[0] = btn_cooldown_press

def btn2_action():
    global alarm_time, display, alarm_activated

    print('--- btn2 released ---')
    if (btn_cooldown[1] > 0): 
        print('btn2 cooldown at ', btn_cooldown[1], ', leaving action')
        return

    if (alarm_ringing):
        alarm_ring_off()
        return

    if (alarm_mode_active):
        alarm_time['minute'] = alarm_time['minute'] + 1
        if (alarm_time['minute'] > 59): alarm_time['minute'] = 1
        print('btn1 > alarm minute hour increased to: ', alarm_time['minute'])
    else:
        print('setting alarm')
        alarm_activated = not alarm_activated
        if (alarm_activated): ledAlarm.on()
        else: ledAlarm.off()
        print('led alarm and alarm activated set to: ', ['false', 'true'][alarm_activated])


    update_display()
    btn_cooldown[1] = btn_cooldown_press

def btn3_action():
    global display

    print('--- btn3 released ---')
    if (btn_cooldown[2] > 0): 
        print('btn3 cooldown at ', btn_cooldown[2], ', leaving action')
        return

    if (alarm_mode_active):
        print('setting and playing sound')
        alarm_set_sound((alarm_sound_index+1) % len(alarm_sounds))
        alarm_play_sound()
        print('sound play call finished')
    else:
        print('setting brightness')
        if (display.brightness-brightness_rate <= 0):
            display.brightness = 1
        else:
            display.brightness = (display.brightness - brightness_rate)

        display_show_brightness()
        print('new brightness set to: ', display.brightness)
    
    btn_cooldown[2] = btn_cooldown_press

def btn2_action_held():
    btn_cooldown[1] = btn_cooldown_hold

    if (alarm_mode_active):
        alarm_mode(False)
        print('alarm ring time: ', alarm_time)
    else:
        alarm_mode(True)

# This function is the mainloop of the program.
# Uses a timer on the current thread to pause the clock every second,
# allowing for blinking of the colon
def main_callback():
    global brightness_screen_time_left, btn_cooldown

	# call timer at start to ensure precise 1 second intervals. If it
	# started at end of function, would be off by a few milliseconds
    threading.Timer(1.0, main_callback).start()

	# check/switch screen for brightness and screen for time
    if (brightness_screen_time_left > 0):
        brightness_screen_time_left -= 1
    else:
        update_time()
        update_display()

	# cooldown for button press to prevent accidental multiple clicks
	# for a button click
    print('updating cooldowns [start]')
    if (btn_cooldown[0] > 0): 
        print('reducing btn1 cooldown')
        btn_cooldown[0] -= 1
    if (btn_cooldown[1] > 0): 
        print('reducing btn2 cooldown')
        btn_cooldown[1] -= 1
    if (btn_cooldown[2] > 0): 
        print('reducing btn3 cooldown')
        btn_cooldown[2] -= 1
    print('updating cooldowns [finish]')
	
	# play sound on alarm ring
    if (alarm_ringing):
		# loop sound when done playing
        if (not alarm_sound.is_alive()):
            alarm_play_sound()
            print('[alarm ringing] replaying alarm ring sound because it finished')

### SETTING PART VALUES

# leds
ledAlarm.off()



### BUTTONS

# button 1
# PRESS -> toggle 24H / 12H
# PRESS [WHEN IN ALARM CHANGE MODE] -> increase alarm time by 1 hour
btn1.when_deactivated = btn1_action

# button 2 is the alarm button.
# HOLD -> enter/exit alarm change mode
# PRESS -> activate/deactivate alarm
# PRESS [WHEN IN ALARM CHANGE MODE] -> increase alarm time by 1 minute
btn2.hold_repeat = False
btn2.hold_time = 1
btn2.when_deactivated = btn2_action
btn2.when_held = btn2_action_held

# button 3
# PRESS -> decrease brightness by 1 level
# PRESS [WHEN IN ALARM CHANGE MODE] -> cycle through alarm ring sound
btn3.when_deactivated = btn3_action

print('finished setting up all components')

### mainloop
# display_show_brightness()
main_callback()

# signal.pause() allows the buttons to continue to monitor and wait for
# button presses
signal.pause()
