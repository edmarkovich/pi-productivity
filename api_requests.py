import requests
import secrets
import datetime

def get_gmail_count():
    url     ="https://www.googleapis.com/gmail/v1/users/"+secrets.CAL1+"/messages?labelIds=INBOX"
    headers ={"Authorization": "Bearer "  +secrets.GMAIL_TOKEN}
    r =requests.get(url, headers=headers)
    
    if r.status_code != 200:
        print("get_gmail_count issue: ", status_code, r.text)
        return -1
    messages= r.json()['messages']
    threads=set()
    for msg in messages:
        threads.add(msg['threadId'])
    threads = len(threads)
    print ("get_gmail_count: Threads: ", threads)
    return threads


def get_task_state(previous_task_count, previous_count_time):
    headers = {"User-Agent": "curl/7.51.0"}
    r =requests.get(secrets.TASKS_URL, headers=headers)
    print(secrets.TASKS_URL)
    if r.status_code != 200:
        print("get_task_state issue: ", r.status_code, r.text)
        return -1

    count = 0
    done  = 0

    for line in r.text.split("\n"):
        print("...", line)
        if "[X]" in line: done  = done  + 1


    now = datetime.datetime.now()
    percent_done = done / (count+done)
    
    if count != previous_task_count:
        previous_task_count = count
        previous_count_time = now
        good_with_tasks = True
    else:
        diff = now - previous_count_time
        good_with_tasks = diff.seconds < 60*60*3
        
    print("Tasks", count, "previous", previous_task_count, "done:" , done)
    return good_with_tasks, percent_done, previous_task_count,previous_count_time


