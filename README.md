# pi-productivity





## What is this?
I am more focused and productive with physical "nudges" in my environment pointing where I should be paying attention. This software/hardware combination parses my **Gmail Inbox, Google Calendars and To-Do File in Dropbox** and uses **LED lights attached to a Raspberry Pi** to flags neglected areas.

This is really useful if you think about your emails, appointments and tasks slimilarly to how I do, which I briefly describe below. These aren't simple notifiers but carefully tailored strategic reminders.

## Warning
If you actually want to make this for yourself, there are two technical hurdles to overcome.
- Raspberry PI hardware stuff - if you have done simple things like connecting an LED to the Pi, you should be fine.
- Dealing with the Google API dashboard to setup an 'application' that's permissioned for Gmail and Gcal, then going through Oauth flows manually to get the token to configure this program with. That only has to be done once but I found the learning curve steep (a few days.) See **configuration** section below.


## Hardware and Software
Out of the box, this code should run on any Raspberry Pi with Python 3, 4 LEDs and a switch button wired up to GPIO pins. If you're doing this, I assume you already know how to connect basic electronics (eg using resistors so your LEDs don't blow up.)

Otherwise, little code here is Pi specific - for example all the code that connects to APIs and applies logic to determine where attention is needed can be run on any system.

![LED Closeup](pics/led-closeup.png)
![Shield Closeup](pics/shield-closeup.png)

In my latest implementation, I soldered the electronics onto a shield board that attaches directly over the Pi. However, that's an aesthetic choice and mainly an excuse to solder. The funcionality can be achieved using a solderless breadboard with a few resistors, LEDs and a button, as seen in this earlier [prorotype](pics/breadboard-closeup.png) (rubberband optional.)



## Functionality

| Source | LED Action | Why |
| :--- | :--- | :--- |
| Gmail Inbox | Yellow LED is lit if any message is older than 24 hours | I archive messages as I read/respond to them. If a message sits in my inbox that long, it means I am resisting dealing with it. The yellow light calls me out.
| Google Calendar | If an event exists on either calendar within the next 24 hours, a blue light comes on intermetedly. The frequency is proportional to time to event - from flashing briefly every few seconds when the event is far off, to steady on when the event is in progress | I don't use my personal calendar much so don't check it frequently. The blue light is signal that something is coming up, prompting me to check the calendar. 
| TODO on Dropbox | Red light is on if the number of unfinished tasks has not changed in 3 hours. Otherwise the light is green | I should be paying attention to tasks I defined for myself earlier. If number of unfinished tasks has not changed, it's a sign I am neglecting this.
| | On button press, the LEDs briefly indicate what percentage of all tasks are done, and flash the specific number of tasks done | This is both to provide a quick insight into my progress and to provide a fun/interactive aspect.

### Calendars
- The blue LED behavior is driven by a pair of calendars - my personal and one I share with my wife. The frequency of the light is based on hwo far away the soonest event is on either calendar. If neither calendar has an event in the next 24 hours, the blue light is off.

### TODO List
- I synch my todo list using Dropbox, and this program accesss it using a URL over HTTP. So there's nothing Dropbox specific about the implementation. It can be any file accessible over the web.
- My TODO list is a free-form file, actually an ASCII table, though yours doesn't have to be. This program considers any line with characters "[ ]" (bracket-space-bracket) in it as an undone item, and any line with "[X]" as a done item.  Both of these patterns are configurable.
- On each refresh, the program checks the number of currently-undone tasks to the previous number. If the number hasn't changed in 3 hours (this is configurable), it lights up the red LED.
- If the number has changed recently, the green LED lights instead. This can be because I checked items as done or even added new items. Either way, I am engaging with the tasks which is good.
- When the program is restarted, the green light will always be on for the first three hours since there's nothing to compare it to. I could have persisted the previous counts but who cares.
- When I press the button, the meaning of LEDs briefly changes to show how much progress I am making on my tasks.
-- First, the number of lights will indicate how I am doing overall:
--- 1 light = 25% of tasks done.
--- 2 lights = 50% done.
--- 3 lights = 75% done.
--- 4 lights = 100% done.
--- An LED will flash rather than steady on if I am close but not quite at the next percentage.
-- Then, the program will flash out the exact number of completed tasks: 
--- Each flash of the red LED indicates 10 tasks are done
--- Each flash of the green LED indicates one task done.
--- Example: 23 completed tasks, that will result in 2 red flashes and 3 green flashes.

### Refresh Frequency
- By default, the code will poll for email, calendar and task list updates every hour. This is configurable.
- You can force a refresh by pressing and holding the button. Let go of the button once all lights are on solid.

## Configuration

### src/secrets.py

You must create a file called **secrets.py** which should define the following variables:
- The url of the tasks file somewhere on the web (eg in your Dropbox share)

**TASKS_URL=""**

- IDs of your Google Calendars. In the simple case of personal, the id is just your email address.

**CAL1=""**
**CAL2=""**

- These are set by following Google's OAUTH processes using Curl or Postman.
This documentation should help but it's quite fiddly.
https://developers.google.com/identity/protocols/oauth2/native-app
At the end of the day, you need to end up with a Google application
permissioned for Gmail and Google Calendar, and an authenticated
refresh token that you will define here.

**REFRESH_TOKEN=""**

**CLIENT_ID=""**

**CLIENT_SECRET=""**

## src/config.py
You can change settings in  [src/config.py](src/config.py) to change:
- Which GPIO pins the lights and button are wired to. **Note: you must either use the same numbers in your setup or change these settings** 
- Refresh frequency
- Thresholds for the lights to come on
- Pattern to recognize done and undone tasks


