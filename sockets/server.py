import socket
import threading
import signal
import sys
import os
import time
from Tkinter import *

####### Action Items #######
# 1. Receive function: data is not printing on GUI Text box

def sendthread(c, top, T):
    def evaluate(event):
        print "serverT> ", str(entry.get())
        input_data = str(entry.get())
        entry.delete(0, END)
        c.send(input_data)
        T.tag_configure("right", background="PaleGreen2", foreground="gray1",justify='right')
        T.insert(END, input_data+'\n', "right")
#        T.tag_add("right","1.0","end")

    entry = Entry(top, text="input here", width=44)
    entry.bind("<Return>", evaluate)
    entry.pack(side=BOTTOM, expand=YES, fill=X)
    entry.place(x=0, y=360)

def receivethread(c, T):
    while True:
        data = c.recv(1024)
        if not data:
            print "Disconnected from client...!"
            sys.exit(1)
        else:
            print "serverR> ", data
            T.tag_configure("left", background="SkyBlue1", foreground="gray1",justify='left')
            T.insert(END, data+'\n', "left")


def signal_handler(sig, frame):
    print "You pressed Ctrl+C"
    sys.exit(0)

if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "Socket created successfully"
    
    port = 5000
    
    s.bind(('', port))
    print "Socket binded to %s" %(port)
    
    s.listen(5)
    print "Socket is listening"
    
    clients = []
    while True:
        c, addr = s.accept()
        clients.append(addr)
        print "clients: ", clients[0]
        print "Got connection from", addr
        user = "Connected to "+addr[0] 
        c.send("Welcome to the messenger")

        pid = os.fork()
        if pid:
            top = Tk()
            top.title("Server chat")
            top.geometry('400x400')
            S = Scrollbar(top)
            T = Text(top, height=25, width=50)
            T.pack(side=TOP, fill=Y)
            T.config(yscrollcommand=S.set)
            T.place(x=0,y=0)
            S.pack(side=RIGHT, fill=Y)
            S.config(command=T.xview)
            T.tag_configure("center", font=("Caliber", 12, "bold"), foreground="orange", justify=CENTER)
            T.insert(END, user+'\n',"center")
            th3 = threading.Thread(target=receivethread, args=(c, T))
            th3.daemon = True
            th3.start()
            th2 = threading.Thread(target=sendthread, args=(c, top, T))
            th2.daemon = True
            th2.start()
            top.mainloop()
            signal.signal(signal.SIGINT, signal_handler)
        else:
            while True:
                time.sleep(1)

#    c.close()
