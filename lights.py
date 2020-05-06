import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
TIME_PIN=4
RED_PIN=12
GREEN_PIN=26
YELLOW_PIN=17
    
GPIO.setup(TIME_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)

def all_on():
    GPIO.output(TIME_PIN, True)
    GPIO.output(RED_PIN, True)
    GPIO.output(GREEN_PIN, True)
    GPIO.output(YELLOW_PIN, True)


def flash_time(hours):
    if hours<0 or hours > 23:
        GPIO.output(TIME_PIN, False)        
        time.sleep(1)
    else:
        GPIO.output(TIME_PIN, True)
        time.sleep(0.2)
        GPIO.output(TIME_PIN, False)
        time.sleep(0.3*hours)

def light_show():
    for x in range(0,110):
        pin = 0
        rnd = random.randint(0,3)
        if rnd==0:   pin=YELLOW_PIN
        elif rnd==1: pin=GREEN_PIN
        elif rnd==2: pin=RED_PIN
        elif rnd==3: pin=TIME_PIN
        GPIO.output(pin, random.randint(0,1))
        time.sleep(.05)
    GPIO.output(YELLOW_PIN, False)

def light_scan()
    
def show_task_status(status):
    dur = 0.05
    if status:
         GPIO.output(YELLOW_PIN, False)
         time.sleep(dur)
         GPIO.output(TIME_PIN, False)
         time.sleep(dur)
         GPIO.output(RED_PIN, False)
         time.sleep(dur)
         GPIO.output(GREEN_PIN, False)
         time.sleep(dur)
         for x in range(0,6):
            GPIO.output(YELLOW_PIN, True)
            time.sleep(dur)
            GPIO.output(TIME_PIN, True)
            time.sleep(dur)
            GPIO.output(RED_PIN, True)
            time.sleep(dur)
            GPIO.output(GREEN_PIN, True)
            time.sleep(dur)
            GPIO.output(YELLOW_PIN, False)
            time.sleep(dur)
            GPIO.output(TIME_PIN, False)
            time.sleep(dur)
            GPIO.output(RED_PIN, False)
            time.sleep(dur)
            GPIO.output(GREEN_PIN, False)
            time.sleep(dur)
         GPIO.output(GREEN_PIN, True)
    else:
            GPIO.output(RED_PIN, True)
            GPIO.output(GREEN_PIN, False)
    time.sleep(2)
            
