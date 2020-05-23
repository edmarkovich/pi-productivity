# pi-productivity





## What is this?
I am more focused and productive with physical "nudges" in my environment pointing where I should be paying attention. This software/hardware combination parses my **Gmail Inbox, Google Calendars and To-Do File in Dropbox** and uses **LED lights attached to a Raspberry Pi** to raise flags to neglected areas.

This is only really useful if you think about your emails, appointments and tasks limilarly to how I do. I will provide a brief overview of my approach below.

## Hardware and Software
Out of the box, this code should run on any Raspberry Pi with Python 3, 4 LEDs and an optional switch button wired up to configurable GPIO pins. If you're doing this, I assume you already know how to connect basic electronics (eg using resistors so your LEDs don't blow up.) However, relatively little code here is Raspberry-Pi specific - for example all the code that connects to APIs and applies logic to determine where attention is needed can be run on any system.

![LED Closeup](pics/led-closeup.png)
![Shield Closeup](pics/shield-closeup.png)

In my latest implementation, I soldered the electronics onto a shield board that attaches directly over the Pi. However, that's an aesthetic choice and mainly an excuse to solder. The funcionality can be achieved using a solderless breadboard with a few resistors, LEDs and a button, as seen in this earlier [prorotype](pics/breadboard-closeup.png). Frayed rubberband optional.



## What it Does

| Source | LED Action | Why |
| :--- | :--- | :--- |
| Gmail Inbox | Yellow LED is lit if any message in the inbox is older than 24 hours | I Practice Inbox-Zero which means I archive messages as I read and respond to them. If a message has sat in my inbox for over 24 hours read or unread, it means I am resisting deciding what to do with it. The yellow light reminds me to bite the bullet and go deal with it.
| Google Calendar | If an event exists on either calendar within the next 24 hours, a blue light comes on intermetedly. The frequency of the light is proportional to how soon the next event is - light flashes briefly every few seconds when the event is far off, to being on steadily when the event is in progress | Unlike work, I don't use my personal Calendar all that much so don't check it frequently as I may only have a handful of events a week if that. So the blue light is a signal that something is happening in the next few hours, prompting me to check the calendar. This program actually polls two calendars - personal and shared with my wife. The logic works using the earliest event on either.
| TODO list on Dropbox | Red light is on if the number of unfinished tasks has not changed in the last 3 hours | During the evenings and weekends, I should be paying attention to tasks I had defined for myself earlier. If the number of unfinished tasks has not changed in 3 hours, it's a good sign I am neglecting this - as tasks should be pretty small and doable within that time window. Note - if the number of tasks has gone __up__ that's still fine as it means I am still engaging with my todos - likely breaking a chunky work item into smaller ones.
