import Tkinter as tk
import Tkinter
from Tkinter import *
import ttk
import os
import fnmatch
import tkFileDialog

from pygame import mixer
import pygame
from pygame.locals import *
import sys
import threading

from PIL import ImageTk, Image
from mutagen import File
from mutagen.mp3 import MP3

# Pending in creation of music progressbar #
def play_track(val):
    global num_tracks
    global i
    global total_s
    i = val
    pygame.init()
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)
    
    audio = MP3(folder[i])
    total_s = audio.info.length
    total_m = total_s / 60
    remain_s = total_s % 60
    print "Min: %d Sec: %d  TotalSec: %d" %(total_m, remain_s, total_s)
    pygame.mixer.music.load(folder[i])
    pygame.mixer.music.play()
    print folder[i]
    
    if pygame.mixer.music.get_busy() == 1:
        pauseb["text"] = "Pause"
    	
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
    	        if num_tracks != i+1:
    	            i += 1
    	        pygame.mixer.music.load(folder[i])
    	        pygame.mixer.music.play()


def album(i):
    print "i value in album: ", i

    file = File(folder[i])
    artwork = file.tags['APIC:'].data
    print "Fetching image details"
    with open('image.jpg', 'wb') as img:
        img.write(artwork)

    path = "image.jpg"
    resize = Image.open(path).resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resize)
    print "Showing image details"
    panel = tk.Label(root, image=img)
    panel.image=img
    panel.pack(side="bottom", fill="both", expand="yes")
    panel.place(x=100,y=400, width=200,height=200)
    
def progress():
    music_progress = tk.StringVar()
    bar = ttk.Progressbar(root, orient="horizontal", mode='determinate', length=500)
    bar.place(x=0,y=200)
    label = ttk.Label(root, textvariable=music_progress)
    label.pack()
    music_progress.set('venky')



if __name__ == "__main__":

    i = 0
    j = 0
    total_s = 0
    path="image.jpg"

    class VerticalScrolledFrame(tk.Frame):
        """A pure Tkinter scrollable frame that actually works!

        * Use the 'interior' attribute to place widgets inside the scrollable frame
        * Construct and pack/place/grid normally
        * This frame only allows vertical scrolling
        """
        def __init__(self, parent, *args, **kw):
            tk.Frame.__init__(self, parent, *args, **kw)            

            # create a canvas object and a vertical scrollbar for scrolling it
            vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
            vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
            canvas = tk.Canvas(self, bd=0, highlightthickness=0,yscrollcommand=vscrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
            vscrollbar.config(command=canvas.yview)

            # reset the view
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)

            # create a frame inside the canvas which will be scrolled with it
            self.interior = interior = tk.Frame(canvas)
            interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

            # track changes to the canvas and frame width and sync them,
            # also updating the scrollbar
            def _configure_interior(event):
                # update the scrollbars to match the size of the inner frame
                size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
                canvas.config(scrollregion="0 0 %s %s" % size)
                if interior.winfo_reqwidth() != canvas.winfo_width():
                    # update the canvas's width to fit the inner frame
#                    canvas.config(width=interior.winfo_reqwidth())
                    canvas.config(width=400, height=400)
                    canvas.pack(padx=1, pady=2, side="right")
            interior.bind('<Configure>', _configure_interior)

            def _configure_canvas(event):
            	if interior.winfo_reqwidth() != canvas.winfo_width():
                    # update the inner frame's width to fill the canvas
                    canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            canvas.bind('<Configure>', _configure_canvas)


    root = tk.Tk()
    root.title("Scrollable Frame Demo")
    root.geometry('700x700')
    root.configure(background="gray99")

    scframe = VerticalScrolledFrame(root)
    scframe.pack()

    folder = []
    directory = []

    def show_values(val):
        val = float(val)
        val = val * 0.1
        pygame.mixer.music.set_volume(val)

    def set_pos(val):
	global total_s
        total_m = total_s / 60
        remain_s = total_s % 60
        print "Min: %d Sec: %d  TotalSec: %d" %(total_m, remain_s, total_s)
#        val = float(val)
#        val = length * val

    def play(i):
        print "i in play: ", i
    	th1 = threading.Thread(target=play_track, args=(i,))
    	th1.start()
        th2 = threading.Thread(target=album, args=(i,))
        th2.start()
#    	th1.join()


    
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please choose the music file directory')
    if len(tempdir) > 0:
        print "You chose %s" % tempdir
   
#    for base, dirnames, filenames in os.walk(tempdir):
    for base, dirnames, filenames in os.walk("/home/venkatesh/Music"):
        for filename in fnmatch.filter(filenames, "*.mp3"):
            folder.append(os.path.join(base, filename))
            directory.append(filename)
            
    for i, x, in enumerate(directory):
        btn = tk.Button(scframe.interior, height=0, width=60, bg="black", 
    	fg="skyblue", text=str(x),command=lambda i=i,x=x: play(i))
    	btn.pack(padx=0, pady=0, side=tk.TOP)
    
    w1 = Tkinter.Scale(root, orient='horizontal', from_=1, to=10, command=show_values)
    w1.pack(padx=0,pady=0, side=tk.TOP)
    w1.place(x=0,y=120)

    w2 = Tkinter.Scale(root, orient='vertical', from_=1, to=10, command=set_pos)
    w2.pack(padx=0,pady=0, side=tk.TOP)
    w2.place(x=0,y=170)

    prevb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Prev", command=lambda: prev_track())
    prevb.pack(padx=0,pady=0,side=tk.LEFT)
    prevb.place(x=0,y=0)
    
    pauseb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Pause", command=lambda: pause())
    pauseb.pack(padx=0,pady=0,side=tk.LEFT)
    pauseb.place(x=0,y=25)
    
    nextb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Next", command=lambda: next_track())
    nextb.pack(padx=0,pady=0,side=tk.LEFT)
    nextb.place(x=0,y=50, anchor=NW)
    
    close = tk.Button(heigh=0, width=10, bg="blue", fg="white", text="Close", command=lambda: close_window())
    close.pack(padx=0,pady=0,side=tk.LEFT)
    close.place(x=0,y=75)
    
    print "Total Number of tracks: ",len(directory)
    num_tracks = len(directory)


    def close_window ():
        os._exit(1)

    pygame.mixer.init()

    def pause():
        if pauseb["text"] == "Pause":
            pauseb["text"] = "Play"
            pygame.mixer.music.pause()
        else:
            pauseb["text"] = "Pause"
            pygame.mixer.music.unpause()


    def next_track():
        global i
        if num_tracks == i+1:
            i = 0
        else:
            i += 1
    	print "next_track: ", i
        pygame.mixer.music.load(folder[i])
        print folder[i]
        pygame.mixer.music.play()

    def prev_track():
        global i
        if i == 0:
            i = num_tracks
        else:
            i -= 1
    	print "prev_track: ", i
        pygame.mixer.music.load(folder[i])
        print folder[i]
        pygame.mixer.music.play()

    root.mainloop()
