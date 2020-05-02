import datetime
import subprocess
import RPi.GPIO as GPIO
import atexit
import time

def cleanup():
    GPIO.cleanup()
    print("BYE")

atexit.register(cleanup)
GPIO.setmode(GPIO.BCM)

TIME_PIN=4
GPIO.setup(TIME_PIN, GPIO.OUT)

def time_to_next_appt():
    #TODO: I think there's a python lib for this
    sp = subprocess.Popen("./pull_agenda", shell=True, stdout=subprocess.PIPE)
    st = sp.stdout.read().strip().decode("ASCII")

    if st == '':
        print ("no apointment?")
        return -1
    
    #print(st)
    
    appt = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
    #this won't work right near new years eve but who cares
    appt = appt.replace(year=datetime.datetime.now().year)

    now = datetime.datetime.now()
    diff = appt - now

    out= (diff.days*24 + diff.seconds/(60*60))
    #print(out)
    return(out)


def flash_time(hours):
    if hours<0 or hours > 23:
        GPIO.output(TIME_PIN, False)        
        return
    while True:
        GPIO.output(TIME_PIN, True)
        time.sleep(0.05)
        GPIO.output(TIME_PIN, False)
        time.sleep(0.2*hours)
    
        

dur = time_to_next_appt()
flash_time(dur)
