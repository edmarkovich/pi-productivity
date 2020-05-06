import RPi.GPIO as GPIO
import time
import random

TIME_PIN=4
RED_PIN=12
GREEN_PIN=26
YELLOW_PIN=17
    
GPIO.setup(TIME_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)

def all_on(state):
    GPIO.output(TIME_PIN, state)
    GPIO.output(RED_PIN, state)
    GPIO.output(GREEN_PIN, state)
    GPIO.output(YELLOW_PIN, state)


def flash_time(hours):
    if hours<0 or hours > 23:
        GPIO.output(TIME_PIN, False)        
        time.sleep(1)
    else:
        GPIO.output(TIME_PIN, True)
        time.sleep(0.2)
        GPIO.output(TIME_PIN, False)
        time.sleep(0.3*hours)


def flash_pin(pin):
             GPIO.output(pin, True)
             time.sleep(.10)
             GPIO.output(pin, False)

def light_show():
    for x in range(0,10):
        for pin  in [YELLOW_PIN, TIME_PIN, RED_PIN, GREEN_PIN]:
            flash_pin(pin)
    for x in range(0,10):
        for pin  in [GREEN_PIN,RED_PIN,TIME_PIN,YELLOW_PIN]:
            flash_pin(pin)
    GPIO.output(YELLOW_PIN, False)

    
def show_task_status(status):
        GPIO.output(RED_PIN, not status)
        GPIO.output(GREEN_PIN, status)
        time.sleep(2)
            
