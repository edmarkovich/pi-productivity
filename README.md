# pi-productivity





## What is this?
I am more focused and productive with physical "nudges" in my environment pointing where I should be paying attention. This software/hardware combination parses my **Gmail Inbox, Google Calendars and To-Do File in Dropbox** and uses **LED lights attached to a Raspberry Pi** to flag neglected areas.

This is a personal hardware/software project and requires some fiddling if you want to use it yourself. I call out what that takes in this file (start with the **Warning**.) My goals were to create this for myself and to learn in the process. Both were achieved. I have this running on my desk all the time. It's useful if you think about productivity similar to me. I briefly describe my philosphy in the **Functionality** section.

The physical product looks like this. You can of course make it look however you want.

![LED Closeup](pics/led-closeup.png)
![Shield Closeup](pics/shield-closeup.png)


## Warning
If you want to make this for yourself, there are two technical hurdles to overcome.
- Raspberry PI hardware stuff - if you can wire up an LED and a button, you will be fine.
- Google API/Oauth setup - only has to be done once but I found the learning curve steep (a few evenings.) See **configuration** section below.

## Functionality

### At a Glance

| Source | LED Action | Philosophy |
| :--- | :--- | :--- |
| Gmail Inbox | Yellow LED is lit if any message is older than 24 hours | I archive messages as I read/respond to them. If a message sits in my inbox that long, it means I am resisting dealing with it. The yellow light calls me out.
| Google Calendar | If an event exists on either calendar within the next 24 hours, a blue light comes on intermittently. The frequency is proportional to time to event - from flashing briefly every few seconds when the event is far off, to steady on when the event is in progress | I don't use my personal calendar much so don't check it frequently. The blue light is a signal that something is coming up, prompting me to check the calendar. 
| TODO on Dropbox | Red light is on if the number of unfinished tasks has not changed in 3 hours. Otherwise the light is green | I should be paying attention to tasks I defined for myself earlier. If the number of unfinished tasks has not changed, it's a sign I am neglecting this.
| | On button press, the LEDs briefly indicate what percentage of all tasks are done, and flash the specific number of tasks done | This is both to provide a quick insight into my progress and to provide a fun/interactive aspect.

### Functionality Details and Caveats

#### Gmail
- The way Gmail works, if any message from a thread is in your Inbox, all messages from that thread are in your inbox. Thus a new message may pull old messages from the thread back in, and so the yellow light will come on next time time the program refreshes. I haven't found this to be a frequent occurance.

#### Calendars
- The blue LED behavior is driven by a pair of calendars - my personal and one I share with my wife. The frequency of the light is based on how far away the soonest event is on either calendar. If neither calendar has an event in the next 24 hours, the blue light is off.

#### TODO List
- I synch my todo list using Dropbox, and this program pulls it over HTTPS. So there's nothing Dropbox specific about the implementation. It can be any file accessible over the web.
- My TODO list is a free-form file, actually an ASCII table, though yours doesn't have to be. This program considers any line with characters "[ ]" (bracket-space-bracket) in it as an undone item, and any line with "[X]" as a done item.  Both of these patterns are configurable.
- On each refresh, the program checks the number of currently-undone tasks to the previous number. If the number hasn't changed in 3 hours (this is configurable), it lights up the red LED.
- If the number has changed recently, the green LED lights instead. This can be because I checked items as done or even added new items. Either way, I am engaging with the tasks which is good.
- When the program is restarted, the green light will always be on for the first three hours since there's nothing to compare it to. I could have persisted the previous counts but who cares.
- When I press the button, the meaning of LEDs briefly changes to show how much progress I am making on my tasks.
  - First, the number of lights will indicate how I am doing overall:
    - 1 light = 25% of tasks done.
    - 2 lights = 50% done.
    - 3 lights = 75% done.
    - 4 lights = 100% done.
    - An LED will flash rather than steady on if I am close but not quite at the next percentage.
  - Then, the program will flash out the exact number of completed tasks: 
    - Each flash of the red LED indicates 10 tasks are done
    - Each flash of the green LED indicates one task done.
    - Example: 23 completed tasks, that will result in 2 red flashes and 3 green flashes.

## Hardware
This code expects: 
- Raspberry Pi with Python 3. I develop on Raspberry Pi 3 but should be fine with earlier versions.
- 4 LEDs wired to GPIO pins via resistors. The defaul pins are listed/changed in [/src/config.py](/src/config.py)
- Switch button wired up to GPIO pins. This isn't strictly needed. I use the button to show more information about tasks and force a data refresh.
- Internet connectivity.

If you're doing this, I assume you already know how to connect basic electronics (eg using resistors so your LEDs don't blow up) so I am not providing any guidance 🙂

In my latest implementation, I soldered the electronics onto a shield board that attaches directly over the Pi. However, that's an aesthetic choice and mainly an excuse to solder. The functionality can be achieved using a solderless breadboard with a few resistors, LEDs and a button, as seen in this earlier [prorotype](pics/breadboard-closeup.png) (rubberband optional.)

## Software
Other than code dealing with lighting LEDs and processing button presses, nothing here is Pi-specific. All the code that connects to APIs and applies logic to determine where attention is needed can be run on any system with Python 3.

- Gmail and Google Calendars are polled using REST APIs. It does not implement the Oath authentication workflows - you have to do that once yourself and provide the token to the program. See the **configuration** section below.
- The task list is accessed using a simple HTTPS request and is therefore much simpler technically. If you want to use just the task functionality, you can comment out the other stuff. I will maybe make that configurable in the future.

### Refresh Frequency
- By default, the code will poll for email, calendar and task list updates every hour. This is configurable.
- You can force a refresh by pressing and holding the button. Let go of the button once all lights are on solid.

## Configuration

### src/secrets.py

You must create a file called **secrets.py** which should define the following variables:
- The url of the tasks file somewhere on the web (eg in your Dropbox share)

```
TASKS_URL=""
```

- IDs of your Google Calendars. In the simple case of a personal calendar, the id is just your email address. Note, the program expects two calendars right now, I should really make this configurable.

```
CAL1=""
CAL2=""
```

- Google REST API Oauth authentication parameters
  - These are obtained by following Google's Oauth processes. 
  - https://developers.google.com/identity/protocols/oauth2/native-app
  - You need to both set up the API and authenticate using Curl or Postman. 
  - This documentation should help but it's quite fiddly if you're new to this as I was.
  - At the end of the day, you need to end up with a Google application client id and client secret along with a live refresh token and provide them here:

```
REFRESH_TOKEN=""
CLIENT_ID=""
CLIENT_SECRET=""
```

### src/config.py
You can change settings in [src/config.py](src/config.py) to control:
- Which GPIO pins the lights and button are wired to.
  - **Note: you must either use the same pins in your setup or change these settings** 
- Refresh frequency
- Thresholds for the lights to come on
- Pattern to recognize done and undone tasks

## Running it
- **Make sure to follow the configuration section above** or you will be instantly disappointed.
- The basic way to run this is just `python3 src/productivity.py`
- I run this on a headless Pi in a `screen` session. the [run](run) script is what I execute inside of `screen`. This redirects error and output into `/tmp/productivity` which I look at when troubleshooting.
  - In order to save wear and tear on the SD card, my `/tmp` is mounted as a ram disk. 
  - As I run the Pi headless, I execute a few other commands to minimize power draw and keep the Pi as cool as possible using the [low-power](low-power) script. This likely doesn't make any actual difference.
