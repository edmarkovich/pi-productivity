
# How Frequently do we refresh
apiPollFrequencyHours = 1

# Light up email light if email is more stale than this
emailAgeThresholdHours = 24

# How many days ahead to look on the calendar. Any events
# older than this will not cause the light to blink
calendarDaysOfNotice   = 1

# If calendar event contains this text in summary, don't notify for it
calendarEventsToSkip   = "Jamie Class"

# How to recognize done and undone tasks
tasksDoneLineContains   = "[X]"
tasksUnDoneLineContains = "[ ]"

# How long can our task count remain unchanged before the light comes on
tasksInactivityThresholdHours = 3


# These are the GPIO Pins on our Raspberry Pi to which lights and buttons are wired.
BUTTON_PIN=27
TIME_PIN=12
RED_PIN=13
GREEN_PIN=19
YELLOW_PIN=18
