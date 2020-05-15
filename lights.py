import RPi.GPIO as GPIO
import time
import random

TIME_PIN=12
RED_PIN=13
GREEN_PIN=19
YELLOW_PIN=18
    
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
        gradual_on(TIME_PIN,True)
        gradual_on(TIME_PIN,False)
        time.sleep(0.3*hours)


def gradual_on(pin, state):
    if state:
        start = 0
        end   = 100
        step  = 20
    else:
        start = 100
        end   = 0
        step  = -20

    #pwm = GPIO.PWM(pin, 100)
    #pwm.start(start)
    #for x in range(start,end,step):
    #    pwm.ChangeDutyCycle(x)
    #    time.sleep(0.05)
    #pwm.stop()
    GPIO.output(pin, state)

def blink(pin, count):
    for x in range(0, count):
        gradual_on(pin, True)
        time.sleep(0.1)
        gradual_on(pin, False)
        time.sleep(0.1)

def show_percentile(value, pin, light_threshold, flash_threshold):
   if value>light_threshold:
        gradual_on(pin, True)
        time.sleep(0.05)
   elif value>flash_threshold:
        blink(pin,10)

def show_percentage(percentage):
    all_on(False)
    time.sleep(0.5)
    percentage = percentage*100
    print("Percentage", percentage)
    
    show_percentile(percentage, GREEN_PIN, 25, 12.5)
    show_percentile(percentage, RED_PIN,   50, 37.5)
    show_percentile(percentage, TIME_PIN,  75, 62.5)
    show_percentile(percentage, YELLOW_PIN, 100, 87.5)
    time.sleep(1) 

    if percentage == 100:
        gradual_on(YELLOW_PIN, False)
        time.sleep(0.1)
    if percentage > 75:
        gradual_on(TIME_PIN, False)
        time.sleep(0.1)
    if percentage > 50:
        gradual_on(RED_PIN, False)
        time.sleep(0.1)
    if percentage > 25:
        gradual_on(GREEN_PIN, False)

    time.sleep(0.1)

def show_task_status(status):
        GPIO.output(RED_PIN, not status)
        GPIO.output(GREEN_PIN, status)
        time.sleep(0.7)
            
