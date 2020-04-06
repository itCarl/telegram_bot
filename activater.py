import os
import sched, time
from datetime import datetime


s = sched.scheduler(time.time, time.sleep)
waitTime = 10


def execPy(sc):
    print("executed telegram bot @ " + datetime.now().strftime("%H:%M:%S"))
    os.system('python3.8 telegram_bot.py')
    s.enter(waitTime, 1, execPy, (sc,))

execPy(s)

s.enter(waitTime, 1, execPy, (s,))
s.run()
