''' Description: Program that acts as a timer that also knows if it has been closed.
 The original idea was for the timer to call shutdown /s /t 1 when either the
 time was up or when the user tried to close the program, which would a)
 make sure the user did not spend more than a certain amount of time on their
 machine, and b) ensure that the user would not try to get out of it. This
 program will only work on Windows.

 To run: See A.py

 Date: 2021/03/30
 Author: Jeremy Hare-Chang
 '''
import socket
import time
from multiprocessing import shared_memory
from datetime import datetime
from os import system

# Check if A is still answering (if so, returns True)
def checkreply(buf):
    if buf[0] == 0:
        buf[0] = 1
        return True
    else:
        return False

# Sends the name of the shared memory module
# to localhost at port 65000. Returns the response
# (which should be the same)
def connectA(name):
    # Note: This may not work if port 65000
    # is taken
    HOST = '127.0.0.1'
    PORT = 65000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(name.encode('utf-8'))
        data = s.recv(1024)
        return data

# We use shared memory for rapid IPC. connectA()
# could have been implemented with shared memory,
# but this program could be refitted to work on
# different machines using just sockets (if
# the following code also used sockets
# and you were so inclined)
shm = shared_memory.SharedMemory(name=None, create=True, size=1)
connected = connectA(shm.name)

# If the other node returned something other than the 
# name it was sent, abort
if connected.decode('utf-8') != shm.name:
    print('Failed to connect.')
    shm.close()
    shm.unlink()
    input()
    quit()
else:
    print(f'Connected!')

start = datetime.now()
while True:
    now = datetime.now()
    # We speed up our checks for replies if
    # Every time we read a reply on shm.buf,
    # sleep for a second to shave processor usage
    if checkreply(shm.buf):
        system('cls')
        start = datetime.now()
        print('received reply from A')
        time.sleep(1)
    # Assume A has been shut down if
    # it does not reply in 3 seconds
    elif (now - start).seconds >= 3:
        break
    else:
        system('cls')
        print(f'No reply from A; will wait {3 - (now - start)} more seconds')

print('system("shutdown /t 1")')
input()