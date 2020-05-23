# pi-productivity





## What is this?
I am more focused and productive with physical "nudges" in my environment pointing where I should be paying attention. This software/hardware combination parses my **Gmail Inbox, Google Calendars and To-Do File in Dropbox** and uses **LED lights attached to a Raspberry Pi** to raise flags to neglected areas.

This is only really useful if you think about your emails, appointments and tasks limilarly to how I do. I will provide a brief overview of my approach below.

## Hardware and Software
Out of the box, this code should run on any Raspberry Pi with Python 3, 4 LEDs and an optional switch button wired up to configurable GPIO pins. If you're doing this, I assume you already know how to connect basic electronics (eg using resistors so your LEDs don't blow up.) However, relatively little code here is Raspberry-Pi specific - for example all the code that connects to APIs and applies logic to determine where attention is needed can be run on any system.

![LED Closeup](pics/led-closeup.png)
![Shield Closeup](pics/shield-closeup.png)

In my latest implementation, I soldered the electronics onto a shield board that attaches directly over the Pi. However, that's an aesthetic choice and mainly an excuse to solder. The funcionality can be achieved using a solderless breadboard with a few resistors, LEDs and a button, as seen in this earlier [prorotype](pics/breadboard-closeup.png). Frayed rubberband optional.



## Functionality

| Source | LED Action | Why |
| :--- | :--- | :--- |
| Gmail Inbox | Yellow LED is lit if any message is older than 24 hours | I archive messages as I read/respond to them. If a message has sat in my inbox that long, it means I am resisting deciding what to do with it. The yellow light reminds me to deal with it.
| Google Calendar | If an event exists on either calendar within the next 24 hours, a blue light comes on intermetedly. The frequency is proportional to time to event - from flashing briefly every few seconds when the event is far off, to steady on when the event is in progress | I don't use my personal calendar much so don't check it frequently. The blue light is signal that something is coming up in the next few hours, prompting me to check the calendar. 
| TODO list on Dropbox | Red light is on if the number of unfinished tasks has not changed in the last 3 hours. Otherwise the light is green | During the evenings and weekends, I should be paying attention to tasks I had defined for myself earlier. If number of unfinished tasks has not changed, it's a sign I am neglecting this.
| | On button press, the LEDs briefly indicate what percentage of all tasks are done, and flash the specific number of tasks done | This is both to provide a quick insight into my progress and to provide a fun/interactive aspect to the thing. It's also a good gamification mechanism for productivity. Each checked-off task leads to one more flash of the counter. 

### Calendars
The blue LED behavior is actually connected to a pair of calendars - my personal and one I share with my wife. The frequency of the blue light is based on far away the soonest event is on either calendar. If neither calendar has an event in the next 24 hours, the blue light is off.

### TODO List
- I synch my todo list using Dropbox, and this program accesss it using a URL over HTTP. So there's nothing Dropbox specific about the implementation. It can be any file accessible over the web.
- My TODO list is a free-form file, actually an ASCII table, though yours doesn't have to be. This program considers any line with characters "[ ]" (bracket-space-bracket) in it as an undone item, and any line with "[X]" in it as a done item.  Both of these patterns are configurable.
- On each refresh, the program checks the number of currently-undone tasks to the previous number. If the number hasn't changed in 3 hours (this is configurable), it lights up the LED. Note that __changed__ could mean that there are now more undone tasks than before. This is fine because it means I had engaged with my todo list in some way - perhaps by breaking a task into smalle tasks.
- When the program is restarted, the green light will always be on for the first three hours.
- When I press the button, the meaning of LEDs briefly changes to show how much progress I am making on my tasks. One light = 25% of tasks done. Two lights = 50% done. 3 lights = 75% done and 4 lights = 100% done. An LED will flash if I am close but not quire at the next percentage. After this display, the program will notify me with the specific number of tasks that are complete. Each flash of the red LED indicates 10 tasks are done, and a green light will count individual tasks. So if I have completed 23 tasks, that will be 2 red flashes and 3 green flashes. This is just for fun gamification.

### Refresh Frequency
- By itself, the code will poll for email, calendar and task list updates every hours. You can force a refresh by pressing and holding the button. Let go of the button once all lights are on solid and it will call all the APIs.

## Configuration
You should create a file called secrets.py which should define the following variables:

The url of the tasks file somewhere on the web (eg in your Dropbox share)
** TASKS_URL="" **

IDs of your Google Calendars. In the simple case of personal, the id is just your email address.
**CAL1=""**
**CAL2=""**

These are set by following Google's OAUTH processes using Curl or Postman.
This documentation should help but it's quite fiddly.
https://developers.google.com/identity/protocols/oauth2/native-app
At the end of the day, you need to end up with a Google application
permissioned for Gmail and Google Calendar, and an authenticated
refresh token that you will define here.

**REFRESH_TOKEN=""**
**CLIENT_ID=""**
**CLIENT_SECRET=""**






Modify [src/config.py](src/config.py) to change:
- Which GPIO pins the lights and button are wired to
- Refresh frequency
- Thresholds for the lights to come on
- Pattern to recognize done and undone tasks


