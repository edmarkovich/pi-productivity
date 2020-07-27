import requests
import secrets
import datetime
import time
import config
from datetime import timezone

def get_google_api_token():
    url    = "https://oauth2.googleapis.com/token"
    params = {"client_id"    :secrets.CLIENT_ID,
              "client_secret":secrets.CLIENT_SECRET,
              "grant_type"   :"refresh_token",
              "refresh_token":secrets.REFRESH_TOKEN
    }

    r = requests.post(url, params=params)
    if r.status_code != 200:
        print("get_google_api_token issue", r.status_code, r.text)
        return -1
    token = r.json()['access_token']
    print("get_google_api_token returning: ", token)
    return token

def is_gmail_message_stale(token, addr, msgid):
    url     ="https://www.googleapis.com/gmail/v1/users/"+addr+"/messages/"+msgid+"?format=minimal&metadataHeaders=internalDate"
    headers ={"Authorization": "Bearer "  + token}
    r =requests.get(url, headers=headers)

    if r.status_code != 200:
        print("get_gmail_message issue: ", r.status_code, r.text)
        return -1

    internalDate = int(r.json()['internalDate']) / 1000
    ageInHours = (int(time.time()) - internalDate)/60/60
    tooOld     = ageInHours > config.emailAgeThresholdHours
    print("get_gmail_message: Age:", ageInHours, "too old: ", tooOld) 
    return tooOld
    
    
def get_stale_gmail_count(token, addr):
    url     ="https://www.googleapis.com/gmail/v1/users/"+addr+"/messages?labelIds=INBOX"
    headers ={"Authorization": "Bearer "  + token}
    r =requests.get(url, headers=headers)

    if r.status_code != 200:
        print("get_gmail_count issue: ", r.status_code, r.text)
        return -1

    if not 'messages' in r.json():
        print("get_gmail_count: no emails!")
        return 0

    messages= r.json()['messages']
    threads=set()
    for msg in messages:
        msgid = msg['id']
        if is_gmail_message_stale(token,addr,msgid):
            threads.add(msg['threadId'])
    threads = len(threads)
    print ("get_gmail_count: Threads: ", threads)
    return threads

def get_calendar_time_to_event(token, cal):

    url     = "https://www.googleapis.com/calendar/v3/calendars/"+cal+"/events"
    headers = {"Authorization": "Bearer "  + token}

    now          = datetime.datetime.utcnow()
    day_from_now = now + datetime.timedelta(days=config.calendarDaysOfNotice)
    
    params  = {
        "singleEvents": "True",
        "timeMin"     : now.isoformat("T") + "Z",
        "timeMax"     : day_from_now.isoformat("T") + "Z",
        "orderBy"     : "startTime"
    }

    r =requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        print("get_calendar_time_to_event: ", r.status_code, r.text)
        return 999


    for item in r.json()['items']:
        if config.calendarEventsToSkip in item['summary']:
            print ("Skipping item with ",  config.calendarEventsToSkip)
            continue

        if 'dateTime' in item['start']:
            start_time = item['start']['dateTime']
            start_time = datetime.datetime.strptime(start_time, 
                "%Y-%m-%dT%H:%M:%S%z")
        else:
            start_time = item['start']['date']
            start_time = datetime.datetime.strptime(
                start_time+"T00:00:00-04:00", "%Y-%m-%dT%H:%M:%S%z")

        diff = start_time - datetime.datetime.now(timezone.utc)
        out = (diff.days*24 + diff.seconds/(60*60))
        print("get_calendar_time_to_event: event in hours: ", out)
        return out
    
    print("get_calendar_time_to_event: no events")
    return 999
    
def get_task_state():
    headers = {"User-Agent": "curl/7.51.0",
               "Authorization": "token "+secrets.TASKS_TOKEN,
               "Accept": "application/vnd.github.v3.raw"}
    r =requests.get(secrets.TASKS_URL, headers=headers)
    if r.status_code != 200:
        print("get_task_state issue: ", r.status_code, r.text)
        return -1

    undone = 0
    done  = 0

    for line in r.text.split("\n"):
        if config.tasksDoneLineContains   in line: done  = done  + 1
        if config.tasksUnDoneLineContains in line: undone  = undone  + 1

    if undone+done == 0:
        print("get_task_state: zero tasks in file")
        return 0,0
        
    print("get_task_state: ", undone, "undone tasks, ", done,"done tasks")
    return undone, done

def get_time_to_next_event_across_calendars(token):
    a=get_calendar_time_to_event(token, secrets.CAL1)
    b=get_calendar_time_to_event(token, secrets.CAL2)
    time_to_event = min(a,b)              #earliest of the two calendars
    time_to_event = max(0, time_to_event) #if event is in progress, delta is negative
    return time_to_event
    


def get_api_states():
    token = get_google_api_token()
    out = {
        'emails':        get_stale_gmail_count(token, secrets.CAL1),
        'time_to_event': get_time_to_next_event_across_calendars(token)
    }
    out['undone_tasks'], out['done_tasks'] = get_task_state()
    return(out)


