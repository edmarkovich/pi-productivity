import datetime
import subprocess

import atexit
import time
import secrets

PC_MODE = False

def cleanup():
    GPIO.cleanup()
    print("BYE")

if not PC_MODE:
    import RPi.GPIO as GPIO
    atexit.register(cleanup)
    GPIO.setmode(GPIO.BCM)

    TIME_PIN=4
    BUTTON_PIN=16
    RED_PIN=12
    GREEN_PIN=26
    
    GPIO.setup(TIME_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, bouncetime=300)        
    
previous_task_count = 0
previous_count_time = 0
last_poll = 0

TASKS_URL = secrets.TASKS_URL
CAL_EMAIL = secrets.CAL_EMAIL

def get_task_state():
    global previous_task_count
    global previous_count_time
    
    cmd = "wget -q -O - " + TASKS_URL + " | fgrep '[ ]' | wc -l"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = sp.stdout.readline().strip().decode("ASCII")
    print("Tasks", count, "previous", previous_task_count)

    now = datetime.datetime.now()

    if count != previous_task_count:
        print ("Nice, the count has changed")
        previous_task_count=count
        previous_count_time=now
        return True

    diff = now - previous_count_time
    print ("Seconds since change: ", diff)
    if diff.seconds > 30:
        return False
    else:
        return True

def time_to_next_appt():
    #TODO: I think there's a python lib for this
    sp = subprocess.Popen("gcalcli --nocolor --calendar="+CAL_EMAIL+" agenda | grep ':' | sed 's/ \+/ /g' | cut -d' ' -f 1-4", shell=True, stdout=subprocess.PIPE)
    
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
        print ("Button press, will refresh")
        return

    now = datetime.datetime.now()
    diff = now - last_poll
    if diff.seconds > 60*60:
        print ("Time elapsed, time to refresh")
        return
    
def show_task_status(status):
    GPIO.output(GREEN_PIN, status)
    GPIO.output(RED_PIN, not status)
    

while True:
    last_poll
    if not PC_MODE:
        GPIO.output(TIME_PIN, True)
        GPIO.output(RED_PIN, True)
        GPIO.output(GREEN_PIN, True)

    try:
        task_status = get_task_state()
        dur = time_to_next_appt()
        last_poll = datetime.datetime.now()
    except Exception as e:
        print ("Something broke", e)

    
    if not PC_MODE:
        show_task_status(task_status)
        flash_time(dur)
    else: break
