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
GPIO.setup(BUTOTN_PIN, GPIO.IN)

def time_to_next_appt():
    #TODO: I think there's a python lib for this
    sp = subprocess.Popen("./pull_agenda", shell=True, stdout=subprocess.PIPE)
    
    while True:
      print(st)
      st = sp.stdout.readline().strip().decode("ASCII")
      if not st: return -1
    
      appt = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
      #this won't work right near new years eve but who cares
      appt = appt.replace(year=datetime.datetime.now().year)

      now = datetime.datetime.now()
      diff = appt - now

      out= (diff.days*24 + diff.seconds/(60*60))
      if out > 0: return out

GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, bouncetime=300)        

def flash_time(hours):
    if hours<0 or hours > 23:
        GPIO.output(TIME_PIN, False)        
        return
    while True:
        GPIO.output(TIME_PIN, True)
        time.sleep(0.05)
        GPIO.output(TIME_PIN, False)
        time.sleep(0.2*hours)
        if GPIO.event_detected(BUTTON_PIN):
            print("Button Press")
            return
    


while True:
    dur = time_to_next_appt()
    flash_time(dur)
