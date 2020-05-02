import datetime
import subprocess
import RPi.GPIO as GPIO
import atexit
import time

def cleanup():
    GPIO.cleanup()
    print("BYE")

atexit.register(cleanup)
GPIO.setup(4, GPIO.OUT)

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


dur = time_to_next_appt()
if dur == -1:
    GPIO.output(4, False)
else:
    GPIO.output(4, True)

    
time.sleep(3)
