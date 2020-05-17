import datetime
import subprocess
import atexit
import time
import secrets
import api_requests

def cleanup():
    GPIO.cleanup()


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import lights

atexit.register(cleanup)

BUTTON_PIN=27
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
previous_task_count = 0
previous_count_time = 0
last_poll = 0



    

def get_task_state():
    global previous_task_count
    global previous_count_time
    
    cmd = "wget -q -O - " + secrets.TASKS_URL # + " | fgrep '[ ]' | wc -l"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    count = 0
    done  = 0

    lines = sp.stdout.readlines()
    for line in lines:
        line = line.strip().decode("ASCII")
        if "[ ]" in line: count = count + 1
        if "[X]" in line: done  = done  + 1
    print("Tasks", count, "previous", previous_task_count, "done:" , done)

    now = datetime.datetime.now()

    if count != previous_task_count:
        previous_task_count = count
        previous_count_time = now
        return True, done / (count+done)

    diff = now - previous_count_time
    return diff.seconds < 60*60*3, done / (count+done)

def time_to_next_appt():
    cmd="gcalcli --nocolor --calendar='"+secrets.CAL1+"' --calendar='"+secrets.CAL2+"' agenda | grep ':' | fgrep -v '(Jamie Class)' | sed 's/ \+/ /g' | cut -d' ' -f 1-4"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    while True:
      st = sp.stdout.readline().strip().decode("ASCII")
      if not st: return -1
      now=datetime.datetime.now() 
      try: 
        appt = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
      except Exception as e:
        #if here, assume for now it's today but 2nd+ item and first is already past
        st = st.split()[0]
        appt = datetime.datetime.strptime(st, '%I:%M%p')
        appt = appt.replace(year = now.year, month = now.month, day = now.day)
      #this won't work right near new years eve but who cares
      appt = appt.replace(year=datetime.datetime.now().year)

      diff = appt - now

      out = (diff.days*24 + diff.seconds/(60*60))
      if out > 0: 
        print ("Next Appt:",appt,out)
        return out

 

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=1000)        
while True:
    lights.all_on(True)
    task_status, task_percentage = get_task_state()
    dur = time_to_next_appt()
    last_poll = datetime.datetime.now()
    gmail=api_requests.get_gmail_count()

    lights.show_percentage(task_percentage)
    lights.show_task_status(task_status, gmail)



    while True:
       lights.flash_time(dur)

       #RE-POLL LOGIC
       if GPIO.event_detected(BUTTON_PIN):
            lights.show_percentage(task_percentage)
            if GPIO.input(BUTTON_PIN) == True:
                print ("Button press, will refresh")
                break
            lights.show_task_status(task_status, gmail)
            continue

       now = datetime.datetime.now()
       diff = now - last_poll
       if diff.seconds > 60*60:
           print ("Time elapsed, time to refresh")
           break
        
