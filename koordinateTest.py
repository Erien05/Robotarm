#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import needed for GUI
import PySimpleGUI as sg

#import needed for serialcommunication
import serial
from time import sleep
import math

#sg.theme("Grey", )

startbyte = 0xEA

#                           +55mm
#servo1 range=(0,110)  +++  150mm
#servo2 range=(20,150) +++  122mm
#servo3 range=(0,180)
#servo4 range=(0,160)  +++   50mm
#servo5 range=(0,40)

layout = [
    [sg.Text('Enter target position')],
    [sg.Text('('), sg.InputText(size =(3, 1)), sg.Text('|'), sg.InputText(size =(3, 1)), sg.Text(')')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Robot Arm', layout)


#start serial
###ser = serial.Serial('/dev/ttyUSB0')

#start quaternionen

add = lambda Q, R: [q+r for q,r in zip(Q, R)]
norm = lambda Q: math.sqrt(sum(q*q for q in Q))
smult = lambda s,Q: [s*q for q in Q]
normalize = lambda Q: smult(1/norm(Q), Q)

def mult(Q,R):
      P = [0, 0, 0, 0]
      for i in range(4):
            for j in range(4):
                  P[abs(i-j) if i*j==0 or i==j else 6-i-j] \
                    += Q[i] * R[j] * (1 if i*j==0 or i%3+1==j else -1)
      return P

#mult([1,3,-2,2], [2,5,-6,3]) -> (1 + 3i + -2j + 2k) * (2 + 5i + -6j + 3k)

conj = lambda q: [q[0]] + [-q[i] for i in range (1, 4)]

def rotate(Punkt, Achse, theta):
      Q = [math.cos(theta/2)] + smult(math.sin(theta/2), normalize(Achse))
      return mult(mult(Q, [0]+Punkt), conj(Q))[1:]

#rotate([4,2,0], [0,0,-1], -math.pi/2) -> drehung des punktes (4,2,0) um -pi/2 um die negative z-Achse

#end quaternionen

event, values = window.read()

while event == 'Submit':

      event, values = window.read()

     #close program
      if event in (sg.WIN_CLOSED, 'Cancel'):
        break


      angle1 = 40
      angle2 = 40
      angle3 = 40
      angle4 = 40
      angle5 = 40

      stepper1 = int(0)


     #serial

      #ser.write(bytearray([angle1]))
      arrVal = bytearray([startbyte, angle1, angle2, angle3, angle4, angle5, stepper1])
      print(arrVal)
###      ser.write(arrVal)


      sleep(0.01)


      print("sending")






window.close()
