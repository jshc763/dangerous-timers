''' Description: Badly named program that
waits argv[1] seconds and keeps updating
the user on its progress


'''

import datetime as dt
import time
from os import system

# Quick and dirty implementation for 'pass by reference'
# aka object attributes
class AsyncSuppressWrapper:
    flag = False

constAswInst = AsyncSuppressWrapper()
constAswInst.flag = False
# Function displays time left until timerlen
# seconds have passed. A forced 'time up'
# announcement may be achieved by setting
# aswArgInstance.flag = True
def startimer(timerlen, aswinstance=constAswInst):
    start = dt.datetime.now()
    while True:
        now = dt.datetime.now()
        # Stop if time is up
        if (now - start).seconds >= timerlen or aswinstance.flag:
            print('Time\'s up!')
            break
        # Let the user know how much time is left
        # and sleep a bit otherwise
        else:
            system('cls')
            print(f'{timerlen - (now - start).seconds} seconds remaining')
        time.sleep(1)

if __name__ == "__main__":
    startimer(1800)

