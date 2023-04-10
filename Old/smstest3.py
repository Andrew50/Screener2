import pywhatkit
import datetime

now = datetime.datetime.now()
hour = now.hour
minute = now.minute + 1
pywhatkit.sendwhatmsg('+19077643274',"test",hour,minute)