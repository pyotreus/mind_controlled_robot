#!/usr/bin/python3
from mindaffectBCI.utopiaclient import *
import serial
import time

microbit_port = 'COM6' #Change port as needed
baud_rate = 115200

# Open the serial connection
ser = serial.Serial(microbit_port, baud_rate, timeout=1)

# Function to send command to micro:bit
def send_command(command):
    ser.write(command.encode('UTF-8') + b'\n')
    time.sleep(0.1)  # Give the micro:bit time to process the command

def doAction(msgs):
    for msg in msgs:
        # skip non-selection messages
        if not msg.msgID==Selection.msgID :
            continue
        try:
            # get the function to execute for selections we are responsible for
            selectionAction = objectID2Actions[msg.objID]
            # run the action function
            selectionAction(msg.objID)
        except KeyError:
            # This is fine, just means it's a selection we are not responsible for
            Pass

# the set of actions to perform
def forward(objID):
    print('move forward')
    send_command('drive')
def backward(objID):
    print('move backward')
    send_command('reverse')
def left(objID):
    print('move left')
    send_command('left')
def right(objID):
    print('move right')
    send_command('right')
def up(objID):
    print('loader up')
    send_command('loader_up')
def down(objID):
    print('loader down')
    send_command('loader_down')

# map from objectIDs to the function to execute
objectID2Actions = { 1:forward, 2:backward, 3:left, 4:right, 5: up, 6: down}

client = UtopiaClient()
client.autoconnect()
client.sendMessage(Subscribe(client.getTimeStamp(),"S"))
while True:
    newmsgs=client.getNewMessages()
    doAction(newmsgs)
