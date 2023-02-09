from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import numpy
import os
from PIL import ImageTk, Image
import cv2
MAXHEIGHT = 250
MAXWIDTH = 250
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
        # self.root = Tk()

        # self.image = cv2.imread(imageNameVal.get())
        self.imageNameVal = imageNameVal
        self.image_label = image_label
        self.brightnessVal = IntVar(root,value=0)
        self.contrastVal = IntVar(root,value=0)
        self.brightnessSlider = Scale(root,from_=-255,to=255,orient='horizontal', variable=self.brightnessVal, command=self.adjustController, length=200,label="Brightness",relief="groove")
        self.contrastSlider = Scale(root,from_=-127,to=127,orient='horizontal', variable=self.contrastVal,command=self.adjustController,length=200,label="Contrast", relief="groove")
        self.brightnessSlider.grid(row=0,column=0)
        self.contrastSlider.grid(row=0,column=1)
    def adjustController(self, *args):
        # image = self.image
        print(self.imageNameVal.get())
        imageNameVal = self.imageNameVal
        image = cv2.imread(imageNameVal.get())
        contrast = self.contrastVal.get()# Contrast control
        brightness = self.brightnessVal.get()# Brightness control

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
        self.root.geometry("700x500")
        self.root.title("My Image Editor")
        self.initializeFrames()
        self.setUpImageSection()
        self.initializeControllers()
        self.setupImageButtons()
        self.root.mainloop()

    def initializeFrames(self):
        root = self.root
        self.mainFrame = Frame(root)
        self.controllerFrame = Frame(root, bg="black", )
        self.mainFrame.pack(fill=X, expand=True, )
        self.controllerFrame.pack( pady=30)

    def setUpImageSection(self,*args):
        mainFrame = self.mainFrame
        self.imageNameVal = StringVar()
        self.imageNameVal.set(TEMPLATEIMG)
        self.image = Image.open(self.imageNameVal.get())
        img = ImageTk.PhotoImage(self.image.resize((MAXHEIGHT,MAXWIDTH)))
        self.image_label = Label(mainFrame, image=img,borderwidth=0)
        self.text_label = Label(mainFrame, text=self.imageNameVal.get())
        self.text_label.pack(pady= 10)
        self.image_label.image = img
        self.image_label.pack(expand=True, pady=15)
    def initializeControllers(self,*args):
        self.imageController = ImageController(self.controllerFrame,self.imageNameVal, self.image_label)

    def setupImageButtons(self,*args):
        imageButtonFrame = Frame(self.mainFrame)
        # imageButtonFrame.grid()
        imageButtonFrame.pack(expand=True,pady=15,side=TOP)
        self.loadImgButton = Button(imageButtonFrame, text="Load", command=self.loadImg, padx=20, bg="black",fg="white")
        self.loadImgButton.grid(row=0, column=0, padx=10)
        self.saveImgButton = Button(imageButtonFrame,text="Save", command=self.saveImg,padx=20, bg="black", fg="white")
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
