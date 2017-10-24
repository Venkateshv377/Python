# explore Tkinter button as simple toggle
import Tkinter as tk  # for Python3 use import tkinter as tk
def toggle_text():
    """toggle button text between Hi and Goodbye"""
    if button["text"] == "Hi":
    	# switch to Goodbye
        button["text"] = "Goodbye"
    else:
        # reset to Hi
        button["text"] = "Hi"
root = tk.Tk()
root.title("Click the Button")

button = tk.Button( text="Hi", width=12, command=toggle_text)
button.pack(padx=100, pady=10)

root.mainloop()
