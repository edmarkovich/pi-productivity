import subprocess
subprocess = subprocess.Popen("./pull_agenda", shell=True, stdout=subprocess.PIPE)
st = subprocess.stdout.read().strip()


#st = "Sun May 03   3:00pm  Plan Out the Week Ahead"
#st = "Sun May 03 3:00pm"

import datetime
date_time_obj = datetime.datetime.strptime(st, '%a %b %d %I:%M%p')
date_time_obj = date_time_obj.replace(year=datetime.datetime.now().year)
print (date_time_obj)

