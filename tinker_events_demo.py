from tkinter import *
from tkinter import ttk
from threading import Thread, Lock
from time import sleep
from random import choice

def events():
    while running:
        sleep(0.5)
        with run_lock:
            if running:
                # Kick off a virtual event
                root.event_generate('<<UPDATE>>')

def update_bar(bar, variance):
    value = bar['value'] + choice(variance)
    if value < 0:
        value = 0
    if value > 100:
        value = 100
    bar['value'] = value

# Virtual event handler
def update_bars(event):
    update_bar(item_1, (-1, 1))
    update_bar(item_2, (-3, -2, 1, 2, 5))
    update_bar(item_3, (-5, -4, -2, 1, 6))

def exit_button_click():
    global running

    with run_lock:
        running = False
        root.destroy()

root = Tk()

frame = ttk.Frame(root, padding = 5)
frame.grid(column = 0, row = 0, sticky = NSEW)

item_1 = ttk.Progressbar(frame, orient = VERTICAL, length = 200, mode = 'determinate', maximum = 100)
item_1.grid(column = 0, row = 0, sticky = EW, padx = 20)
item_1['value'] = 50

item_2 = ttk.Progressbar(frame, orient = VERTICAL, length = 200, mode = 'determinate', maximum = 100)
item_2.grid(column = 1, row = 0, sticky = EW, padx = 20)
item_2['value'] = 50

item_3 = ttk.Progressbar(frame, orient = VERTICAL, length = 200, mode = 'determinate', maximum = 100)
item_3.grid(column = 2, row = 0, sticky = EW, padx = 20)
item_3['value'] = 50

exit_button = ttk.Button(frame, text = 'Exit', command = exit_button_click)
exit_button.grid(column = 0, row = 1, columnspan = 3, sticky = E, pady = 10)

# The virtual event that will be handled
root.bind('<<UPDATE>>', func = update_bars)

run_lock = Lock()

with run_lock:
    running = True

event_thread = Thread(target = events)
event_thread.start()

root.mainloop()
