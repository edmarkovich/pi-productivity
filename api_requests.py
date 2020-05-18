import requests
import secrets
import datetime
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
    
def get_gmail_count(token, addr):
    url     ="https://www.googleapis.com/gmail/v1/users/"+addr+"/messages?labelIds=INBOX"
    headers ={"Authorization": "Bearer "  + token}
    r =requests.get(url, headers=headers)
    
    if r.status_code != 200:
        print("get_gmail_count issue: ", r.status_code, r.text)
        return -1
    messages= r.json()['messages']
    threads=set()
    for msg in messages:
        threads.add(msg['threadId'])
    threads = len(threads)
    print ("get_gmail_count: Threads: ", threads)
    return threads

def get_calendar_time_to_event(token, cal):

    url     = "https://www.googleapis.com/calendar/v3/calendars/"+cal+"/events"
    headers = {"Authorization": "Bearer "  + token}

    now          = datetime.datetime.utcnow()
    day_from_now = now + datetime.timedelta(days=1)
    
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

    if len(r.json()['items']) == 0:
        print("get_calendar_time_to_event: no events")
        return 999

    start_time = r.json()['items'][0]['start']['dateTime']
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")

    diff = start_time - datetime.datetime.now(timezone.utc)
    out = (diff.days*24 + diff.seconds/(60*60))
    print("get_calendar_time_to_event: event in hours: ", out)
    return out
    
    
def get_task_state():
    headers = {"User-Agent": "curl/7.51.0"}
    r =requests.get(secrets.TASKS_URL, headers=headers)
    if r.status_code != 200:
        print("get_task_state issue: ", r.status_code, r.text)
        return -1

    count = 0
    done  = 0

    for line in r.text.split("\n"):
        if "[X]" in line: done  = done  + 1
        if "[ ]" in line: count  = count  + 1

    if count+done == 0:
        print("get_task_state: zero tasks in file")
        return 0,0
        
    percent_done = done / (count+done)
    print("get_task_state: ", count, "undone tasks, ", percent_done,"% done")
    return count, percent_done


def get_api_states():
    token = get_google_api_token()
    out = {}
    out['emails'] = get_gmail_count(token, secrets.CAL1)

    a=get_calendar_time_to_event(token, secrets.CAL1)
    b=get_calendar_time_to_event(token, secrets.CAL2)
    time_to_event = min(a,b)
    out['time_to_event'] = max(0, time_to_event)

    out['undone_tasks'], out['task_percentage'] = get_task_state()
    return(out)


