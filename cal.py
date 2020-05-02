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

def get_task_count():
    cmd = "wget -q -O - https://www.dropbox.com/s/lqnwp6v2agwi3wy/week-plan.org?dl=0 | fgrep '[ ]' | wc -l"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = sp.stdout.readline().strip().decode("ASCII")
    print("Tasks", count)

def time_to_next_appt():
    #TODO: I think there's a python lib for this
    sp = subprocess.Popen("./pull_agenda", shell=True, stdout=subprocess.PIPE)
    
    while True:
      st = sp.stdout.readline().strip().decode("ASCII")
      if not st: return -1
    
      appt = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
      #this won't work right near new years eve but who cares
      appt = appt.replace(year=datetime.datetime.now().year)

      now = datetime.datetime.now()
      diff = appt - now

      out= (diff.days*24 + diff.seconds/(60*60))
      if out > 0: 
        print (out)
        return out

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
    GPIO.output(TIME_PIN, True)
    get_task_count()
    dur = time_to_next_appt()
    flash_time(dur)
