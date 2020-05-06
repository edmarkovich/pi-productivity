import datetime
import subprocess
import atexit
import time
import secrets
import lights

def cleanup():
    GPIO.cleanup()


import RPi.GPIO as GPIO
atexit.register(cleanup)
GPIO.setmode(GPIO.BCM)

BUTTON_PIN=16
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, bouncetime=300)        
    
previous_task_count = 0
previous_count_time = 0
last_poll = 0

def get_task_state():
    global previous_task_count
    global previous_count_time
    
    cmd = "wget -q -O - " + secrets.TASKS_URL + " | fgrep '[ ]' | wc -l"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = sp.stdout.readline().strip().decode("ASCII")
    print("Tasks", count, "previous", previous_task_count)

    now = datetime.datetime.now()

    if count != previous_task_count:
        previous_task_count = count
        previous_count_time = now
        return True

    diff = now - previous_count_time
    return diff.seconds < 60*60*3

def time_to_next_appt():
    cmd="gcalcli --nocolor --calendar='"+secrets.CAL1+"' --calendar='"+secrets.CAL2+"' agenda | grep ':' | fgrep -v '(Jamie Class)' | sed 's/ \+/ /g' | cut -d' ' -f 1-4"
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

      diff = appt - datetime.datetime.now()

      out = (diff.days*24 + diff.seconds/(60*60))
      if out > 0: 
        print ("Next Appt:",appt,out)
        return out

 

while True:
    lights.all_on()

    try:
        task_status = get_task_state()
        dur = time_to_next_appt()
        last_poll = datetime.datetime.now()
    except Exception as e:
        print ("Something broke", e)

    
    lights.light_show()
    lights.show_task_status(task_status)


    lights.flash_time(dur)

    while True:
       #RE-POLL LOGIC
       if GPIO.event_detected(BUTTON_PIN):
           print ("Button press, will refresh")
           break

       now = datetime.datetime.now()
       diff = now - last_poll
       if diff.seconds > 60*60:
           print ("Time elapsed, time to refresh")
           break
        
       time.sleep(2) 
