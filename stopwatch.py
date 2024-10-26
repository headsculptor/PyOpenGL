import threading
import time
from tkinter import *

gui = Tk()
gui.geometry("35x75")

class stopwatch:
    def __init__(self, parent, l_btn, l_lbl):
        self.togglebtn = l_btn
        self.countlbl = l_lbl
        self.to_start_text = "Start"
        self.to_stop_text = "Stop"
        self.togglebtn.config(text = self.to_start_text, command = self.toggle, bg = "lime")
        self.countlbl.config(text = "0.0")
        self.parent = parent
        self.parent.update()
    def toggle(self):
        if self.togglebtn.cget("text") == self.to_start_text:
            self.togglebtn.config(text = self.to_stop_text, bg = "orange")
            self.parent.update()
            self.st = threading.Thread(target = self.stopwatch)
            self.st.start()
        else:
            self.stopwatch_isactive = False
            self.togglebtn.config(text = self.to_start_text, bg = "lime")
            self.parent.update()
    def stopwatch(self):
        try:
            self.stopwatch_isactive = True
            self.x = 0
            while self.stopwatch_isactive == True:
                time.sleep(0.01)
                self.x += 0.01
                self.countlbl.config(text = str(round(self.x, 3)))
                self.parent.update()
        except:
            None
            
btn = Button(gui)
lbl = Label(gui, text = "0.00")
btn.place(x = 38, y = 32)
lbl.place(x = 45, y = 5)
stopwatch(parent = gui, l_btn = btn, l_lbl = lbl)
   
gui.mainloop()
