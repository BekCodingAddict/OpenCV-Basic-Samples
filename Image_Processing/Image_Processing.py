from PyQt5.QtWidgets import QApplication,QMessageBox,QDesktopWidget,QMainWindow,QPushButton,QLabel, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
from scipy import ndimage
import re
import sys
from PIL import Image, ImageEnhance
# from skimage.util import random_noise
from random import randint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # No external window yet for load image function.
        self.w=None
        
        # No external window yet for inputs of crop image function.
        self.inputWindowOfRotation=None

        # chance color balance window
        self.ccbWindow=None
        
        # adjust brightness window
        self.adjBrgWindow=None

        # adjust saturation window
        self.adjSatWindow=None

        # flip image window
        self.flipImage=None

        # adjust contrast windpw
        self.adjConWindow=None

        #Setting Up  x, y coordinates and buttons measurments
        self.warning=None
        xtop=10
        yleft=10
        margin=10
        buttonWidth=150
        buttonHeight=50

        sizeObject=QDesktopWidget().screenGeometry()

        # Access screen dimensions of image - screen accordance
        self.width=int(sizeObject.getRect()[2])
        self.height=int(sizeObject.getRect()[3])

        #Declaration of image size
        self.imgWidth=0
        self.imgHeight=0

        # Set up message area widget
        # This for guiding user when deal with an error 
        self.message=QLabel(self)
        self.message.setFont(QFont("Arial",12))
        self.message.setGeometry(400,50,1450,160)
        self.message.setStyleSheet("color:white; border:3px solid black;  border-color: gray; border-style: outset;  border-width: 2px; border-radius:8px;background-color:hsl(206,90%,74%);")
        self.message.setText("Hello")

        #File text area widget
        hFile=QLabel(self)
        hFile.setText("File")
        hFile.setFont(QFont("Arial",20))
        hFile.move(xtop+int(buttonHeight/4),yleft)

        #load button widget
        #Save Button Widget
        loadButton=QPushButton(self)
        #Set text of button
        loadButton.setText("Load Image")
        #Set button coordinates and its width, height
        loadButton.setGeometry(xtop+20,yleft+buttonHeight,buttonWidth,buttonHeight)
        #Runs function (show_new_window) when clicked button
        loadButton.clicked.connect(self.show_new_window)
        loadButton.setStyleSheet("QPushButton:hover{background-color:green;color:white;} border-radius:5px; border:2px doted black;background-color:green;color:white;")

        #Save button widget
        saveButton=QPushButton(self)
        saveButton.setText("Save Image")
        saveButton.setGeometry(xtop+180,yleft+buttonHeight,buttonWidth,buttonHeight)
        saveButton.clicked.connect(self.save)
        saveButton.setStyleSheet("QPushButton:hover{background-color:green;color:white;};border-radius:5px; border:2px doted black;background-color:green;color:white;")

        #-------EDIT AREA---------
        #Edit text area widget
        hEdit=QLabel(self)
        hEdit.setText("Edit")
        hEdit.setFont(QFont("Arial",20))
        hEdit.move(xtop+int(buttonHeight/4),xtop+110)

        #Blur button widget
        blurButton=QPushButton(self)
        blurButton.setText("Blur Image")
        blurButton.setGeometry(xtop+20,yleft+3*buttonHeight,buttonWidth,buttonHeight)
        blurButton.clicked.connect(self.blur)
        blurButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")


        #Deblur button widget
        deblurButton=QPushButton(self)
        deblurButton.setText("Deblur Image")
        deblurButton.setGeometry(xtop+180,yleft+3*buttonHeight,buttonWidth,buttonHeight)
        deblurButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        deblurButton.clicked.connect(self.deblur)

        #Loaded Image widget
        self.loadedImage=QLabel(self)
        #Scale image for screen accordance
        self.loadedImage.setScaledContents(True)
        self.loadedImage.setFixedHeight(int(self.height/2))
        self.loadedImage.setFixedWidth(int(self.width/3))
        self.loadedImagePath=""
        self.loadedImage.move(400,300)
        self.loadedImage.setStyleSheet("border:5px solid hsl(27,50%,36.9%); border-radius:10px;")


        self.manipulatedImage=QLabel(self)

        self.manipulatedImage.setScaledContents(True)
        self.manipulatedImage.setFixedHeight(int(self.height/2))
        self.manipulatedImage.setFixedWidth(int(self.width/3))
        self.manipulatedImage.move(int(self.width/1.6),300)
        self.manipulatedImage.setStyleSheet("color:white; border:5px solid black;  border-color: gray; border-style: outset; border-radius:8px;background-color:hsl(206,90%,74%);")

        #Set coordinate and size of main screen of application
        self.setGeometry(0,0,self.width,self.height)
        self.setWindowTitle("Final Term OpenCv Image Processing Project")
        # self.setStyleSheet("background-color:hsl(206,100%,60%);")


    def show_new_window(self, checked):
        if self.w is None:
            self.w=QFileDialog.Option()
            fileName,_=QFileDialog.getOpenFileName(self,"Open Image","","All Files(*.jpg *.png *.jpeg)",options=self.w)


            pixmap=QPixmap(fileName)
            pixmap2=pixmap.scaledToWidth(int(self.width/2))
            self.loadedImage.setPixmap(pixmap2)
            self.loadedImage.adjustSize()
            self.loadedImagePath=fileName

        self.w=None

    def save(self):
        try:
            if(len(self.loadedImagePath)==0):
                raise FileNotFoundError 
            self.manipulatedImage.pixmap().save("SavedImage.jpg","JPG")
            self.message.setText("")
        
        except FileNotFoundError:
            self.message.setText("You have to create manipulated image to save it!")
        except Exception as E:
            self.message.setText(str(E))

    def blur(self):
        try:
            #access loaded Image
            image=cv2.imread(self.loadedImagePath)
            if(image is None):
                raise FileNotFoundError

            #Blur Image 
            blurImg=cv2.blur(image(9,9))

            #Save blured image temporarly
            cv2.imwrite("Temp.jpg",blurImg)

            pixmap=QPixmap("./temp.jpg")
            pixmap2=pixmap.scaledToWidth(int(self.width/2))  

            self.manipulatedImage.setPixmap(pixmap2)
            self.manipulatedImage.adjustSize()
            #Set message text to empty, when process s successfull
            self.message.setText("") 
        except FileNotFoundError:
            self.message.setText("You have to Load an Image before Bluring")

        except Exception as E:
            self.message.setText(str(E))

    def deblur(self):
        try:
            image=cv2.imread(self.loadedImagePath)
            if(image is None):
                raise FileNotFoundError
            sharpen_karnel=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
            sharpen=cv2.filter2D(image,-1,sharpen_karnel)

            cv2.imwrite("temp.jpg",sharpen)

            pixmap=QPixmap("./temp.jpg")
            pixmap2=pixmap.scaledToWidth(int(self.width/2))

            self.manipulatedImage.setPixmap(pixmap2)
            self.manipulatedImage.adjustSize()

            self.message.setText("")

        except FileNotFoundError:
            self.message.setText("You have to Load an Image before debluring!")
        except Exception as E:
            self.message.setText(str(E))
            print(E)


app=QApplication(sys.argv)
main=MainWindow()
main.show()
app.exec()

        
