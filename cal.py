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
BUTTON_PIN=16
GPIO.setup(TIME_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
    print(out)
    return(out)

GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, bouncetime=300)        

def flash_time(hours):
  while True:
    if hours<0 or hours > 23:
        GPIO.output(TIME_PIN, False)        
        time.sleep(1)
    else:
        GPIO.output(TIME_PIN, True)
        time.sleep(0.2)
        GPIO.output(TIME_PIN, False)
        time.sleep(0.3*hours)
    if GPIO.event_detected(BUTTON_PIN):
        return
    


while True:
    dur = time_to_next_appt()
    flash_time(dur)
