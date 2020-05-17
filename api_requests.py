import requests
import secrets

def get_gmail_count():
    url     ="https://www.googleapis.com/gmail/v1/users/"+secrets.CAL1+"/messages?labelIds=INBOX"
    headers ={"Authorization": "Bearer "  +secrets.GMAIL_TOKEN}
    print(headers)
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


