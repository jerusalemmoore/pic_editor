#https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
import sys, os
from tkinter import ttk
from PIL import Image as PilImage
from PIL import PSDraw
from tkinter import *
from tkinter import colorchooser

UPARROW =  "\u2191"
DOWNARROW = "\u2193"
# def convertToJPG(image):
#     f, e = os.path.splitext(image)
#     newImage = f + ".jpg"
#     if image != newImage:
#         try:
#             with PilImage.open(image) as im:
#                 im.save(newImage)
#         except OSError:
#             print(OSError)
#             print("cannot convert", image)
#
# convertToJPG("image.jfif")

# main = Tk(screenName="image_editor",sync=True)
# frm = ttk.Frame(main,padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!"). grid(column=0,row=0)
# ttk.Button(frm,text="Quit", command=main.destroy).grid(column=1,row=0)
# main.mainloop()
class MetersFeetConverter:
    def __init__(self, root):
        root.title("Feet/Meter Converter")

        # hold the contents of the interface
        mainframe = Frame(root)
        print(mainframe.configure().keys())
        mainframe.grid(sticky="n s")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.errorMsg = StringVar()
        self.errorMsg.set("")
        self.error_label = Label(mainframe, textvariable=self.errorMsg)
        self.error_label.grid(column=2, row=0)
        self.feet_label = Label(mainframe,text= "Feet")
        self.feet_label.grid(column=1,row=1, padx=(10,10))
        self.feet = StringVar()
        self.feet_entry = Entry(mainframe, width=20, textvariable=self.feet)
        self.feet_entry.grid(column=2, row=1)
        self.to_label = Label(mainframe, text="to")
        self.to_label.grid(column=1, row=3)
        self.meters_label = Label(mainframe,text="Meters")
        self.meters_label.grid(column=1,row=4, padx=(10,10))
        self.meters  = StringVar()
        self.meters_entry = Entry(mainframe, width=20, textvariable=self.meters, state="disabled")
        self.meters_entry.grid(column=2, row=4)
        self.quit_button = Button(mainframe, command=root.destroy, text="Exit")
        self.quit_button.grid(column=4,row=5, padx=(5,5), pady=(5,5))
        self.calc_button = Button(mainframe,command=self.calculate, text="Calculate")
        self.calc_button.grid(column=5, row= 5, padx=(5,5), pady=(5,5))
        self.arrow_button = Button(mainframe, command=self.flip, text=DOWNARROW)
        self.arrow_button.grid(column=2,row=3, pady=(10,10))
        # B2.pack()
        root.mainloop()

    def calculate(self, *args):
        arrowDirection = self.arrow_button.cget('text')
        if arrowDirection == DOWNARROW:
            try:
                value = float(self.feet.get())
                self.meters.set(float(0.3048 * value * 10000.0 + 0.5)/10000.0)
            except ValueError as e:

                print(e)
                print(type(self.feet.get()))
                print(len(self.feet.get()))
                if self.feet.get() == "":
                    self.errorMsg.set("Feet cannot be empty")
                pass
        else:
            try:
                value = float(self.meters.get())
                self.feet.set(float(value * 3.28084))
            except ValueError as e:
                print(e)
                if self.meters.get() == "":
                    self.errorMsg.set("Meters cannot be empty")
                pass
    # flip conversion direction (starts feet to meters)
    def flip(self, *args):
        # downward \u2193
        # upward  \u2191
        arrowDirection = self.arrow_button.cget('text')
        if arrowDirection == UPARROW:
            self.arrow_button.config(text=DOWNARROW)
            self.meters_entry.config(state="disabled")
            self.feet_entry.config(state="normal")
        else:
            self.arrow_button.config(text=UPARROW)
            self.feet_entry.config(state="disabled")
            self.meters_entry.config(state="normal")
root = Tk()
MetersFeetConverter(root)
