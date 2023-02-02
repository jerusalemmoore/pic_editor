from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import numpy

from PIL import ImageTk, Image
import cv2
MAXHEIGHT = 250
MAXWIDTH = 250
class imgEditor:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("700x500")
        self.initializeFrames()
        self.initializeSliders()
        self.setUpImageSection()



        self.root.mainloop()
    def initializeFrames(self):
        root = self.root
        self.mainFrame = Frame(root)
        self.slidersFrame = Frame(root)
        self.colorsFrame = Frame(root)
        self.slidersFrame.pack(side = LEFT)
        self.mainFrame.pack( expand=True)

    def setUpImageSection(self,*args):
        mainFrame = self.mainFrame
        self.imageNameVal = StringVar()
        self.imageNameVal.set("image.jfif")
        img = ImageTk.PhotoImage(Image.open(self.imageNameVal.get()).resize((MAXHEIGHT,MAXWIDTH)))
        self.image_button = Button(mainFrame, image=img,borderwidth=0,command=self.uploadImage)
        self.image_button.image = img
        self.image_button.pack(expand=True)
        text_label = Label(mainFrame, text=self.imageNameVal.get())
        text_label.pack()
    def initializeSliders(self):
        slidersFrame = self.slidersFrame

        self.brightnessVal = IntVar(slidersFrame,value=0)
        self.brightnessSlider = Scale(slidersFrame, from_=-256,to=256,orient='horizontal', variable=self.brightnessVal,command=self.changeBrightness)
        self.brightnessSlider.pack()

    def convertToTkImg(self, image:numpy.ndarray) -> ImageTk.PhotoImage:
        # print("hello")
        blue,green,red = cv2.split(image)
        adjustedImage = cv2.merge((red,green,blue))
        imageData = Image.fromarray(adjustedImage)
        tkinterImage = ImageTk.PhotoImage(imageData.resize((MAXHEIGHT,MAXWIDTH)))
        return tkinterImage

    def changeBrightness(self,*args):
        # print(imageNameVal.get())
        imageNameVal = self.imageNameVal
        image = cv2.imread(imageNameVal.get())
        alpha = 1# Contrast control
        beta = self.brightnessVal.get()# Brightness control
        adjustedImage = cv2.addWeighted(image,alpha,image,0, beta)
        tkinterImage = self.convertToTkImg(adjustedImage)
        self.image_button.config(image=tkinterImage)
        self.image_button.photo = tkinterImage

    def uploadImage(self, *args):
        self.resetSliders()
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select image",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        # print("filename " + filename)
        if filename:
            self.imageNameVal.set(filename)
            new_image = ImageTk.PhotoImage(Image.open(self.imageNameVal.get()).resize((MAXHEIGHT,MAXWIDTH)))
            # new_image.shape
            self.image_button.config(image=new_image)
            self.image_button.photo = new_image
    def resetSliders(self, *args):
        self.brightnessSlider.set(0)

imgEditor()
