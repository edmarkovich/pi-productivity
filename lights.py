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
        flash_pin(TIME_PIN)
        time.sleep(0.3*hours)


def flash_pin(pin):
    pwm = GPIO.PWM(pin, 100)
    pwm.start(0)
    for x in range(0,100,20):
        pwm.ChangeDutyCycle(x)
        time.sleep(0.03)
    time.sleep(.02)
    for x in range(100,0,-20):
        pwm.ChangeDutyCycle(x)
        time.sleep(0.03)
    pwm.stop()
    time.sleep(.02)
   

def light_show():
    for x in range(0,1):
        for pin  in [GREEN_PIN,RED_PIN,TIME_PIN,YELLOW_PIN]:
            flash_pin(pin)
        for pin  in [TIME_PIN, RED_PIN, GREEN_PIN]:
            flash_pin(pin)
    time.sleep(1)

def show_percentage(percentage):
    percentage = percentage*100
    print("Percentage", percentage)
    if percentage > 25:
        flash_pin(GREEN_PIN)
        GPIO.output(GREEN_PIN, True)
    if percentage > 50:
        flash_pin(RED_PIN)
        GPIO.output(RED_PIN, True)
    if percentage > 75:
        flash_pin(TIME_PIN)
        GPIO.output(TIME_PIN, True)
    if percentage == 100:
        flash_pin(YELLOW_PIN)
        GPIO.output(YELLOW_PIN, True)
    time.sleep(2) 
    GPIO.output(GREEN_PIN, False)
    GPIO.output(RED_PIN, False)
    GPIO.output(TIME_PIN, False)
    GPIO.output(YELLOW_PIN, False)
    
def show_task_status(status):
        GPIO.output(RED_PIN, not status)
        GPIO.output(GREEN_PIN, status)
        time.sleep(0.7)
            
