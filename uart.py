#!/usr/bin/env python
from Tkinter import *
import serial
import threading

top = Tk()

def handler(data):
    T.insert(END, data)

def callback(port):
    data = ""
    while(1):
    	data = port.readline().decode()
    	handler(data)
	data = ""

l1 = Label(top, text="Select a serial device", fg="blue")
l1.pack(side='top', expand=True,padx=0,pady=0)
serialdevice = Entry(top)
serialdevice.pack(side='top')
device = serialdevice.get()

l2 = Label(top, text="Baudrate", fg="blue")
l2.pack(side='top', expand=True,padx=0,pady=0)
baud = Entry(top)
baud.pack(side='top')
baudrate = baud.get()

S = Scrollbar(top)
T=Text(top)
T.focus_set()
S.pack(side=RIGHT,fill=Y)
T.pack(side=LEFT,fill=Y)
T.config(yscrollcommand=S.set)


def thread_func():
    port = serial.Serial(serialdevice.get())
    port.baudrate = baud.get()
    thread = threading.Thread(target=callback, args=(port,))
    thread.start()

b=Button(top, text="Show", command=thread_func)
b.pack()
c=Button(top, text='Exit', command=top.destroy)
c.pack()

top.mainloop()
