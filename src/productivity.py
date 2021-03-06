import datetime
import subprocess
import atexit
import time
import secrets
import api_requests
import config

def cleanup():
    GPIO.cleanup()


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import lights

atexit.register(cleanup)


GPIO.setup(config.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(config.BUTTON_PIN, GPIO.RISING, bouncetime=5000)


previous_task_count = 0
previous_count_time = 0
last_poll = 0



def good_with_tasks(count):
    global previous_task_count
    global previous_count_time
    now = datetime.datetime.now()
    print(count, previous_task_count)
    if count != previous_task_count:
        print ("good_with_tasks: task count has changed - good.",
               count, previous_task_count)
        previous_task_count = count
        previous_count_time = now
        return True
    else:
        diff      = now - previous_count_time
        diffHours = diff.seconds / 60 / 60
        diffHours = diffHours + (diff.days * 24)
        weGood    = diffHours <  config.tasksInactivityThresholdHours
        print ("good_with_tasks: hours since last count change:",
               diffHours, weGood)
        return weGood
        
 


error_count=0
while True:
    last_poll = datetime.datetime.now()
    print("~~~~> ", last_poll)
    lights.all_on(True)
    try:
        api_states = api_requests.get_api_states()
        print("Main Loop: API states", api_states)
    except Exception as e:
        error_count = error_count+1
        print("Main Loop: something went wrong with API calls")
        print(e)
        delay = min(error_count*10,60*5) #retry fast, then back off up to 5min
        print ("  Waiting for "+str(delay)+"sec before retrying")
        for x in range(0,delay):
            lights.all_on(True)
            time.sleep(0.5)
            lights.all_on(False)
            time.sleep(0.5)
        continue    
        
    task_status = good_with_tasks(api_states['undone_tasks'])
    lights.show_task_status(task_status, api_states['emails'])


    while True:
       lights.flash_time_to_event(api_states['time_to_event'])

       if GPIO.event_detected(config.BUTTON_PIN):
            print("Main Loop: Button press")
            lights.show_percentage(api_states['undone_tasks'], api_states['done_tasks'])
           
            #Force re-poll logic
            if GPIO.input(config.BUTTON_PIN) == True:
                print ("Main Loop: Button hold, will refresh")
                break            
            else:
                print("Main Loop: Blink Done Tasks: ", api_states['done_tasks'])
                lights.show_done(api_states['done_tasks'])

            lights.show_task_status(task_status, api_states['emails'])
            continue

       now = datetime.datetime.now()
       elapsed_hours = (now - last_poll).seconds / (60*60)
       if elapsed_hours > config.apiPollFrequencyHours:
           print ("Main Loop:", elapsed_hours,"hours elapsed, time to refresh")
           break

        
