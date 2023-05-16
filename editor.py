from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import numpy
import os
from PIL import ImageTk, Image
import cv2
import numpy as np

MAXHEIGHT = 400
MAXWIDTH = 400
# this is a space that tracks changes to image, this is so newly edited images
# aren't overwritten from their original
WORKINGIMG ="current/working.jpg"
TEMPLATEIMG = "image.jfif"
def convertToTkImg(image:numpy.ndarray) -> ImageTk.PhotoImage:
    # print("hello")
    blue,green,red = cv2.split(image)
    adjustedImage = cv2.merge((red,green,blue))
    imageData = Image.fromarray(adjustedImage)
    imageData.save(WORKINGIMG)
    tkinterImage = ImageTk.PhotoImage(imageData.resize((MAXHEIGHT,MAXWIDTH)))
    return tkinterImage
# for contrast and brightness adjustment calculations
# https://www.geeksforgeeks.org/changing-the-contrast-and-brightness-of-an-image-using-python-opencv/
#Scale class that can be used to adjust the brightness of an image label
#   root is the frame we'd like this slider to be packed intor
#   imageNameVal is the name of the image we'd like to change
#   image_label is the visual image who's brightness will be adjusted and presented
class ImageController:
    def __init__(self, root, imageNameVal, image_label):
        self.imageNameVal = imageNameVal
        self.image_label = image_label
        self.brightnessVal = IntVar(root,value=0)
        self.contrastVal = IntVar(root,value=0)
        self.blurVal = IntVar(root,value=0)
        self.sharpnessVal=IntVar(root,value=0)
        self.brightnessSlider = Scale(root,from_=-255,to=255,orient='horizontal', variable=self.brightnessVal, command=self.adjustController, length=200,label="Brightness",relief="raised", bg="grey")
        self.contrastSlider = Scale(root,from_=-127,to=127,orient='horizontal', variable=self.contrastVal,command=self.adjustController,length=200,label="Contrast", relief="raised", bg="grey")
        self.blurSlider = Scale(root,from_=0,to=100, orient='horizontal', variable=self.blurVal,command=self.adjustController,length=200,label="Blur", relief="raised",bg="grey",resolution=3)
        self.sharpnessSlider = Scale(root,from_=0,to=100, orient='horizontal', variable=self.sharpnessVal,command=self.adjustController,length=200,label="Blur", relief="raised",bg="grey")
        self.brightnessSlider.grid(row=0,column=0, padx=5,pady=5)
        self.contrastSlider.grid(row=0,column=1, padx=5, pady=5)
        self.blurSlider.grid(row=1,column=0,padx=5,pady=5)
        self.sharpnessSlider.grid(row=1,column=1,padx=5,pady=5)
    def adjustController(self, *args):
        # image = self.image
        print(self.imageNameVal.get())
        imageNameVal = self.imageNameVal
        image = cv2.imread(imageNameVal.get())
        contrast = self.contrastVal.get()# Contrast control
        brightness = self.brightnessVal.get()# Brightness control
        blur = self.blurVal.get()
        sharpness = self.sharpnessVal.get()
        if brightness != 0:
            print("hi")
            if brightness > 0:
                shadow = brightness
                max = 255
            else:
                shadow = 0
                max = 255 + brightness
            al_pha = (max - shadow) / 255
            ga_mma = shadow
            print(al_pha)
            print(ga_mma)
            adjustedImage = cv2.addWeighted(image,al_pha,image,0,ga_mma)
        else:
            adjustedImage = image
        if contrast != 0:
            print(contrast)
            alpha = float(131*(contrast + 127)) / (127*(131 - contrast))
            gamma = 127 * (1- alpha)
            print(alpha)
            print(gamma)
            adjustedImage = cv2.addWeighted(adjustedImage,alpha,adjustedImage,0,gamma)
        if blur != 0:
            adjustedImage = cv2.medianBlur(adjustedImage,self.blurVal.get())
        if sharpness != 0:
            filter = np.array([[0,0,-1,0,0],[0,-1,5,-1,0],[0,0,-1,0,0]] * sharpness)
            adjustedImage=cv2.filter2D(adjustedImage,-1,filter)
        tkinterImage = convertToTkImg(adjustedImage)
        self.image_label.config(image=tkinterImage)
        self.image_label.photo = tkinterImage
    def resetController(self):
        self.brightnessSlider.set(0)
        self.contrastSlider.set(0)
    def setImage(self,imageNameVal, image_label):
        self.imageNameval = imageNameVal
        self.image_label = image_label

class imgEditor:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x700")
        self.root.title("My Image Editor")
        self.root.config(background="dodgerblue4")
        self.initializeFrames()
        self.setUpImageSection()
        self.initializeControllers()
        self.setupImageButtons()
        self.root.mainloop()

    def initializeFrames(self):
        root = self.root
        self.mainFrame = Frame(root, bg="steelblue", highlightbackground="white", padx=20, highlightthickness=2)
        self.controllerFrame = Frame(root, highlightbackground="white",bg="steelblue", highlightthickness=2, pady=5 )
        self.mainFrame.pack( pady=15)
        self.controllerFrame.pack(pady=20 )

    def setUpImageSection(self,*args):
        mainFrame = self.mainFrame
        self.imageNameVal = StringVar()
        self.imageNameVal.set(TEMPLATEIMG)
        self.image = Image.open(self.imageNameVal.get())
        img = ImageTk.PhotoImage(self.image.resize((MAXHEIGHT,MAXWIDTH)))
        self.image_label = Label(mainFrame, image=img, bg="steelblue")
        self.text_label = Label(mainFrame, text=self.imageNameVal.get(), bg="steelblue",fg="black")
        self.text_label.pack(pady= 10, )
        self.image_label.image = img
        self.image_label.pack(expand=True, pady=15)
    def initializeControllers(self,*args):
        self.imageController = ImageController(self.controllerFrame,self.imageNameVal, self.image_label)

    def setupImageButtons(self,*args):
        imageButtonFrame = Frame(self.mainFrame, bg="steelblue", padx=5, pady=5, highlightbackground="white", highlightthickness=2,relief="groove")
        # imageButtonFrame.grid()
        imageButtonFrame.pack(expand=True,pady=15,side=TOP)
        self.loadImgButton = Button(imageButtonFrame, text="Load", command=self.loadImg, padx=20, bg="grey",fg="black")
        self.loadImgButton.grid(row=0, column=0, padx=10)
        self.saveImgButton = Button(imageButtonFrame,text="Save", command=self.saveImg,padx=20, bg="grey", fg="black")
        self.saveImgButton.grid(row=0,column=1, padx=10)

    def loadImg(self, *args):
        filename = filedialog.askopenfilename(initialdir = "pic_editor_images",title = "Select image",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if filename:
            self.resetController()
            self.imageNameVal.set(filename)
            self.image = Image.open(self.imageNameVal.get())
            new_image = ImageTk.PhotoImage(self.image.resize((MAXHEIGHT,MAXWIDTH)))
            self.image_label.config(image=new_image)
            self.image_label.photo = new_image
            self.text_label.config(text=os.path.basename(self.imageNameVal.get()))
            # self.imageController.setImage(self.imageNameVal, self.image_label)
    def resetController(self, *args):
        self.imageController.resetController()


    def saveImg(self,*args):
        filename = filedialog.asksaveasfilename(initialdir="pic_editor_images", title="Save image as", initialfile="default.jpg", filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        if filename:
            image = Image.open(WORKINGIMG)
            splitFilename = filename.split(".")
            if "jpg" in splitFilename[-1] or "jpeg" in splitFilename[-1]:
                image.save(filename)
            else:
                image.save(filename+".jpg")

imgEditor()
