''' Description: Program that acts as a timer that also knows if it has been closed.
 The original idea was for the timer to call shutdown /s /t 1 when either the
 time was up or when the user tried to close the program, which would a)
 make sure the user did not spend more than a certain amount of time on their
 machine, and b) ensure that the user would not try to get out of it. This
 program will only work on Windows.

 To run: $ python3 A.py <time in seconds>,
 Then $ python3 B.py in that order.

 Date: 2021/03/30
 Author: Jeremy Hare-Chang
 '''
import socket
from multiprocessing import shared_memory
import time
from datetime import datetime
from os import system
import threading
import halfhrtime
import sys

# Check if B is still answering (if so, returns True)
def checkreply(buf):
    if buf[0] == 1:
        buf[0] = 0
        return True
    else:
        return False

# Get name of the shared memory region
def connectB():
    HOST = '127.0.0.1'
    PORT = 65000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: A.py <time in seconds>")
        input()
        quit()

    # Connect to shared memory
    retname = connectB().decode('utf-8')
    try:
        shm = shared_memory.SharedMemory(retname, False, 1)
    except AttributeError:
        print('Could not connect.')
        input()
        quit()


    timerstart = datetime.now()
    start = datetime.now()

    wrapper = halfhrtime.AsyncSuppressWrapper()
    th = threading.Thread(target=halfhrtime.startimer, args=(int(sys.argv[1]), wrapper))
    th.start()
    while True:
        now = datetime.now()
        # Every time we read a reply on shm.buf,
        # sleep for a second to shave processor usage
        if checkreply(shm.buf):
            start = datetime.now()
            time.sleep(1)
        elif (now - start).seconds >= 3:
            print('Didn\'t get reply from B.')
            break

    # Signal to timer to stop printing time
    wrapper.flag = True
    # This would probably be a bad idea
    print('system("shutdown /s /t 1")')
    input()