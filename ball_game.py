import FaBo9Axis_MPU9250
import time
import sys
import Tkinter
from Tkinter import Tk
from Tkinter import Canvas


mpu9250 = FaBo9Axis_MPU9250.MPU9250()
#gyroString = "x:{x:.2f} y:{y:.2f} z:{z:.2f}" 
#gyro = mpu9250.readGyro()

multiplier = 5

min = 25
max = 170

maxVal = 0
minVal = 0

window = Tk()
window.title("welcome")
window.geometry('350x200')
cvs = Canvas(window)
line = cvs.create_line(0,max,350,max, width=10, fill='green')
elipse = cvs.create_oval(175,100,145,130, width=10, fill='green')
cvs.configure(bg="black")
cvs.pack(fill="both", expand=True)

def moveBall():
    print('test')
    vals = cvs.find_overlapping(cvs.bbox(elipse)[0],cvs.bbox(elipse)[1],cvs.bbox(elipse)[2],cvs.bbox(elipse)[3])
    print(vals)
    cvs.move(elipse,0,1)
    cvs.after(50, moveBall)

def normalize(value):
    numer = value-(-250)
    denom = 500
    return numer/denom

def drawLine():
    global maxVal
    global minVal
    print('test')
    gyro = mpu9250.readGyro()
    gyroString = "x:{x:.2f} y:{y:.2f} z:{z:.2f}"
    if(gyro['x'] > maxVal):
        maxVal = gyro['x']
    if(gyro['x'] < minVal):
        minVal = gyro['x']
    print("max:{max1:.2f} min:{min1:.2f}".format(max1=maxVal, min1=minVal))
    print("normalized:{normalx:.2f} ,{normaly:.2f},{normalz:.2f}".format(normalx=normalize(gyro['x']),normaly=normalize(gyro['y']),normalz=normalize(gyro['z'])))
    print(gyroString.format(x=gyro['x'],y=gyro['y'],z=gyro['z']))
    
    if(cvs.coords(line)[1] > min and normalize(gyro['z']) > 0.6):
        cvs.move(line, 0, -(multiplier * normalize(gyro['z'])))
    if(cvs.coords(line)[1] < max and normalize(gyro['z']) < 0.4):
        cvs.move(line, 0, (multiplier * (1 - normalize(gyro['z']))))
    cvs.after(50, drawLine)

drawLine()
moveBall()
window.mainloop()
