# pi-productivity

## What does this do?
I find that I stick to what I need to do better when there's a physical reminder in my space of something I need to be doing or paying attention to. This is a simple project that enables my Raspberry Pi 4 to indicate with state of 4 LED lights.

### Personal Setup
The things that I want to personally be aware of:
- **If there's an email in my gmail inbox older than a day**. I practice inbox-zero so ideally there should not be anything stale in the box. If there is, a light comes on (yellow) to remind me I need to go clean things out. Note that this is not a "you got mail" light - I don't want to be distracted when a message comes in. That's why the light does not come on until the message is a day old, as that means I likely had seen the email and been avoiding deadling with/deleting it.
- **If I had made any progress on my todo list in the last 3 hours**. I break down my tasks projects into small chunks so incremental progress can always be made and going 3 hours without anything getting checked off can be a sign I am not focusing on my projects. In practice, I don't pay attention to this during work hours as I manage my work-tasks differently, but I pay attention to this on the weekends and in the evenints. There's a green light if I had crossed something off or added something to my list in the last 3 hours and otherwise a red light.
- **Whether I have any Calendar events coming up in the next 24 hours**. At work I look at my calendar constantly but my personal calendar is pretty sparse and I don't look at it ofter. So I have a reminder (blue light) that lights up if I have anything coming up in the next 24 hours. The light barely blinks if the apointment is a long time from now and gets a little more intense as the time approaches. The idea is that it forces me to check my calendar to see what it is that I have coming up. 
