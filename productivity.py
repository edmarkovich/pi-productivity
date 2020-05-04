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
CAL1 = secrets.CAL1
CAL2 = secrets.CAL2

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
    if diff.seconds > 60*60*3: #Did nothing for 3 hours?!
        return False
    else:
        return True

def time_to_next_appt():
    #TODO: I think there's a python lib for this
    cmd="gcalcli --nocolor --calendar='"+CAL1+"' --calendar='"+CAL2+"' agenda | grep ':' | sed 's/ \+/ /g' | cut -d' ' -f 1-4"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    while True:
      st = sp.stdout.readline().strip().decode("ASCII")
      if not st: return -1
   
      try: 
        appt = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
      except Exception as e:
        #if here, assume for now it's today but 2nd+ item and first is already past
        st = st.split()[0]
        appt2 = datetime.datetime.strptime(st, '%I:%M%p')
        appt2 = appt2.replace(year = appt.year, month = appt.month, day = appt.day)
        appt = appt2
      #this won't work right near new years eve but who cares
      appt = appt.replace(year=datetime.datetime.now().year)

      now = datetime.datetime.now()
      diff = appt - now

      out= (diff.days*24 + diff.seconds/(60*60))
      if out > 0: 
        print ("Next Appt:",appt,out)
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
    dur = 0.05
    if status:
         GPIO.output(TIME_PIN, False)
         time.sleep(dur)
         GPIO.output(RED_PIN, False)
         time.sleep(dur)
         GPIO.output(GREEN_PIN, False)
         time.sleep(dur)
         for x in range(0,6):
            GPIO.output(TIME_PIN, True)
            time.sleep(dur)
            GPIO.output(RED_PIN, True)
            time.sleep(dur)
            GPIO.output(GREEN_PIN, True)
            time.sleep(dur)
            GPIO.output(TIME_PIN, False)
            time.sleep(dur)
            GPIO.output(RED_PIN, False)
            time.sleep(dur)
            GPIO.output(GREEN_PIN, False)
            time.sleep(dur)
         #time.sleep(0.5)
         GPIO.output(GREEN_PIN, True)
    else:
            GPIO.output(RED_PIN, True)
            GPIO.output(GREEN_PIN, False)
    time.sleep(2) 

while True:
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
