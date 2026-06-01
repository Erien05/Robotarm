#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import needed for GUI
import PySimpleGUI as sg

#import needed for serialcommunication
import serial
from time import sleep

#from Position import quaternionen
#from Position import koordinate
import Position

#sg.theme("Grey", )

startbyte = 0xEA


#xKoordinate, yKoordinate, zKoordinate = update()

#create slider column
slider_column = [
       #servo1
       [sg.Text("servo 1 angle:"), sg.Text(size=(3,1), key="servoval1", enable_events=True)],
       [sg.Slider(orientation ='horizontal', key='servoangle1', range=(35,145), enable_events=True)],
       #servo2
       [sg.Text("servo 2 angle:"), sg.Text(size=(3,1), key="servoval2", enable_events=True)],
       [sg.Slider(orientation ='horizontal', key='servoangle2', range=(50,180), enable_events=True)],
       #servo3
       [sg.Text("servo 3 angle:"), sg.Text(size=(3,1), key="servoval3", enable_events=True)],
       [sg.Slider(orientation ='horizontal', key='servoangle3', range=(0,180), enable_events=True)],
       #servo4
       [sg.Text("servo 4 angle:"), sg.Text(size=(3,1), key="servoval4", enable_events=True)],
       [sg.Slider(orientation ='horizontal', key='servoangle4', range=(100,260), enable_events=True)],
       #servo5
       [sg.Text("servo 5 angle:"), sg.Text(size=(3,1), key="servoval5", enable_events=True)],
       [sg.Slider(orientation ='horizontal', key='servoangle5', range=(0,40), enable_events=True)],
       #stepper1
       [sg.Text("stepper 1 movement")],
       [sg.Button("LEFT"), sg.Button("STOP"), sg.Button("RIGHT")],
       #show koordinate
       [sg.Text("x:"), sg.Text(size=(6,1), key="x"), sg.Text("y:"), sg.Text(size=(6,1), key="y"), sg.Text("z:"), sg.Text(size=(6,1), key="z")],


       ]
       
enter_position = [
    [sg.Text('Enter target position')],
    [sg.Text('('), sg.InputText(size =(4, 1), key="x-input"), sg.Text('|'), sg.InputText(size =(4, 1), key="y-input"), sg.Text('|'), sg.InputText(size =(4, 1), key="z-input"), sg.Text(')')],
    [sg.Submit(), sg.Cancel()]
]


#hole layout
layout = [
       [sg.Button("Start Robot Arm")],
       [sg.Column(slider_column)],
       [sg.Column(enter_position)]
       ]


#create window
window = sg.Window('Robot Arm', layout)

#start serial
ser = serial.Serial('/dev/ttyUSB0')

event, values = window.read()
#start position from main.c file
window.Element('servoangle1').update(60+35)
window.Element('servoangle2').update(60+30)
window.Element('servoangle3').update(90)
window.Element('servoangle4').update(80+100)
window.Element('servoangle5').update(10)

while True:
      event, values = window.read()

     #close program
      if event == "Exit" or event == sg.WIN_CLOSED or event == "Cancel":
        break
    
      if event == "Start Robot Arm":
        print("Sarting ...")
     #serial_for_one_servo
    # window['stVal'].update(int(values['stSlider']))
     #a=int(values['stSlider'])
     #ser.write(bytearray([a]))
     #print("sending " + str(a))
     #sleep(0.01)
     
     #define servo angles for arduino
        #window['servoval1'].update(int(values['servoangle1']))
      angle1 = int(values['servoangle1'])
      angle2 = int(values['servoangle2'])
      angle3 = int(values['servoangle3'])
      angle4 = int(values['servoangle4'])
      angle5 = int(values['servoangle5'])
      if event in ("LEFT"):
        stepper1 = int(1)
      elif event in ("RIGHT"):
        stepper1 = int(2)
      elif event in ("STOP"):
        stepper1 = int(0)
      else:
        stepper1 = int(0)
        
      xyzKoordinate = Position.angleToKoordinate(angle1, angle2, angle3, angle4, stepper1)
      xKoordinate = xyzKoordinate[0]
      yKoordinate = xyzKoordinate[1]
      zKoordinate = xyzKoordinate[2]
      #x = xKoordinate
      window.Element('x').update(xKoordinate)
      window.Element('y').update(yKoordinate)
      window.Element('z').update(zKoordinate)

      if event == "Submit":
        x_input = int(values['x-input'])
        y_input = int(values['y-input'])
        z_input = int(values['z-input'])

        angles = Position.koordinateToAngles([x_input, y_input, z_input])

        angle1 = angles[0]
        angle2 = angles[1]
        angle3 = angles[2]
        angle4 = angles[3]
        stepper = angles[4]

        window.Element('servoangle1').update(angle1)
        window.Element('servoangle2').update(angle2)
        #window.Element('servoangle3').update(angle3)
        window.Element('servoangle4').update(angle4)

     
     #serial 
     
      arrVal = bytearray([startbyte, angle1 - int(35), angle2 - int(30), angle3, angle4 - int(100), angle5, stepper1])
      print(arrVal)
      #stepper1 = int(0) ##### nach der while schleife wieder auf 0 setzen damit er nicht permanent dreht
      ser.write(arrVal)
      
      
      sleep(0.01)
   
      #print("sending")
     
    
      
     

     
window.close()
