import Tkinter as tk
import os
import fnmatch

#from pygame import mixer
import pygame
from pygame.locals import *


j = 0

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
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


root = tk.Tk()
root.title("Scrollable Frame Demo")
root.configure(background="gray99")

scframe = VerticalScrolledFrame(root)
scframe.pack()

global pygame
directory = os.walk("/home/venkatesh/Music/Music").next()[2]
pygame.mixer.init()

for i, x in enumerate(directory):
    btn = tk.Button(scframe.interior, height=0, width=60, 
        bg="gray99", fg="purple3", text=str(x),
        command=lambda i=i,x=x: play(i))
    btn.pack(padx=0, pady=0, side=tk.TOP)


prevb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Prev",
	command=lambda i=i,x=x: prev_track(i))
prevb.pack(padx=0,pady=0,side=tk.LEFT)

pauseb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Pause",
	command=lambda i=i,x=x: pause(i))
pauseb.pack(padx=0,pady=0,side=tk.LEFT)

nextb = tk.Button(heigh=0, width=10, bg="blue",fg="white",text="Next",
	command=lambda i=i,x=x: next_track(i))
nextb.pack(padx=0,pady=0,side=tk.LEFT)


print "Total Number of tracks: ",len(directory)
def play(i):
    global j
    j = i
    pygame.mixer.music.load('/home/venkatesh/Music/Music/' + directory[i])
    pygame.mixer.music.play()

    if pygame.mixer.music.get_busy() == 1:
    	pauseb["text"] = "Pause"
    i += 1
    pygame.mixer.music.queue('/home/venkatesh/Music/Music/' + directory[i])

def pause(a):
    if pauseb["text"] == "Pause":
    	pauseb["text"] = "Play"
	pygame.mixer.music.pause()
    else:
    	pauseb["text"] = "Pause"
	pygame.mixer.music.unpause()


def next_track(n):
    global j
    j += 1
    pygame.mixer.music.load('/home/venkatesh/Music/Music/' + directory[j])
    pygame.mixer.music.play()

def prev_track(p):
    global j
    j -= 1
    pygame.mixer.music.load('/home/venkatesh/Music/Music/' + directory[j])
    pygame.mixer.music.play()

root.mainloop()
