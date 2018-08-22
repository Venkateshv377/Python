#!/usr/bin/python
import socket
import threading
import signal
import time
import sys
from Tkinter import *
from math import *

###### Action Items #######
# 1. Receive function: Data is not printing on GUI Text box 

def recievethread(s, T):
    while True:
        data = s.recv(1024)
        if not data:
            print "Disconnected from server...!"
            sys.exit(1)
        else:
            print "clientR>", data
            T.tag_config("left", background="SkyBlue1", foreground="gray1", justify="left")
            T.insert(END, data+'\n', "left")

def sendthread(s, sr, T):
    def evaluate(event):
        print "clientT> ", str(entry.get())
        input_data = str(entry.get())
        entry.delete(0, END)
        print "input_data", input_data
        s.send(input_data)
        T.tag_config("right", background="PaleGreen2", foreground="gray1", justify="right")
        T.insert(END, input_data+'\n', "right")

    entry = Entry(sr, text="input here", width=44)
    entry.bind("<Return>", evaluate)
    entry.pack(side=TOP, expand=YES, fill=X)
    entry.place(x=0, y=360)

def signal_handler(sig, frame):
    print "You pressed Ctrl+C"
    sys.exit(1)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "Socket created successfully"
    port = 5000
    host = '127.0.0.1'
    host2 = '192.168.2.15'
    s.connect((host2, port))
    print "connection done"
    s.send("Welcome to the messenger")

    sr = Tk()
    sr.title("Client chat")
    sr.geometry('400x400')
    S = Scrollbar(sr)
    T = Text(sr, height=25, width=50)
    T.pack(side=TOP, fill=Y)
    T.config(yscrollcommand=S.set)
    T.place(x=0,y=0)
    S.pack(side=RIGHT, fill=Y)
    S.config(command=T.yview)
    T.tag_configure("center", font=("Caliber", 12, "bold"),foreground="orange", justify=CENTER)
    T.insert(END, s.recv(1024)+'\n', "center")
    th2 = threading.Thread(target=recievethread, args=(s, T))
    th2.daemon = True
    th2.start()
    th3 = threading.Thread(target=sendthread, args=(s, sr, T))
    th3.daemon = True
    th3.start()
    sr.mainloop()

#    th2 = threading.Thread(target=receive, args=(s,))
#    th2.daemon = True
#    th2.start()
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(1)
#    s.close()

