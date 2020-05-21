import RPi.GPIO as GPIO
import time
import random
import config
    
GPIO.setup(config.TIME_PIN, GPIO.OUT)
GPIO.setup(config.RED_PIN, GPIO.OUT)
GPIO.setup(config.GREEN_PIN, GPIO.OUT)
GPIO.setup(config.YELLOW_PIN, GPIO.OUT)

def all_on(state):
    GPIO.output(config.TIME_PIN, state)
    GPIO.output(config.RED_PIN, state)
    GPIO.output(config.GREEN_PIN, state)
    GPIO.output(config.YELLOW_PIN, state)


def flash_calendar_time_to_event(hours):
    if hours<0 or hours > config.calendarDaysOfNotice*24:
        GPIO.output(config.TIME_PIN, False)        
        time.sleep(1)
    else:
        gradual_on(config.TIME_PIN,True)
        time.sleep(0.2)
        gradual_on(config.TIME_PIN,False)
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
        return True
   return False

def show_percentage(percentage):
    all_on(False)
    time.sleep(1)
    percentage = percentage*100
    
    blinked = show_percentile(percentage, config.GREEN_PIN, 25, 12.5)
    blinked = blinked or show_percentile(percentage, config.RED_PIN,   50, 37.5)
    blinked = blinked or show_percentile(percentage, config.TIME_PIN,  75, 62.5)
    blinked = blinked or show_percentile(percentage, config.YELLOW_PIN, 100, 87.5)
    if not blinked: time.sleep(1) 
    all_on(False)
    time.sleep(1)


def show_task_status(status, gmail):
        got_mail = (gmail != 0)
        GPIO.output(config.RED_PIN, not status)
        GPIO.output(config.GREEN_PIN, status)
        GPIO.output(config.YELLOW_PIN, got_mail)
            
