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
        
        #No external window yet for inputs of crop image function
        self.inputWindow=None
        # No external window yet for inputs of rotate image function
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

        #Reverse Color Button Widget
        reverseColorButton=QPushButton(self)
        reverseColorButton.setText("Reverse Color")
        reverseColorButton.setGeometry(xtop+20,(yleft+yleft)+(4*buttonHeight),buttonWidth,buttonHeight)
        reverseColorButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        reverseColorButton.clicked.connect(self.reverseColor)

        #Grayscale button widget
        grayScaleButton=QPushButton(self)
        grayScaleButton.setText("GrayScale Image")
        grayScaleButton.setGeometry(xtop+180,(yleft+yleft)+(4*buttonHeight),buttonWidth,buttonHeight)
        grayScaleButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        grayScaleButton.clicked.connect(self.grayScale)
        

        #Crop button widget
        cropButton=QPushButton(self)
        cropButton.setText("Crop Image")
        cropButton.setGeometry(xtop+20,yleft*3+5*buttonHeight,buttonWidth,buttonHeight)
        cropButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        cropButton.clicked.connect(self.crop)

        #Flip button widget
        flipButton=QPushButton(self)
        flipButton.setText("Flip Image")
        flipButton.setGeometry(xtop+180,yleft*3+5*buttonHeight,buttonWidth,buttonHeight)
        flipButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        flipButton.clicked.connect(self.flip)

        #Mirror button widget
        mirrorButton=QPushButton(self)
        mirrorButton.setText("Mirror Image")
        mirrorButton.setGeometry(xtop+20,yleft*4+6*buttonHeight,buttonWidth,buttonHeight)
        mirrorButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        mirrorButton.clicked.connect(self.mirror)

        #Rotate button widget
        rotateButton=QPushButton(self)
        rotateButton.setText("Rotate Image")
        rotateButton.setGeometry(xtop+180,yleft*4+6*buttonHeight,buttonWidth,buttonHeight)
        rotateButton.setStyleSheet("border-radius:5px; border:2px doted black;background-color:green;color:white;")
        rotateButton.clicked.connect(self.rotate)



        #Loaded Image widget
        self.loadedImage=QLabel(self)
        #Scale image for screen accordance
        self.loadedImage.setScaledContents(True)
        self.loadedImage.setFixedHeight(int(self.height/2))
        self.loadedImage.setFixedWidth(int(self.width/3))
        self.loadedImagePath=""
        self.loadedImage.move(400,300)
        self.loadedImage.setStyleSheet("border:5px solid hsl(27,50%,36.9%); border-radius:10px;")

        #Manipulate Image Widget
        self.manipulatedImage=QLabel(self)
        #Scale image for screen accordance
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
            #Get FileName of image
            fileName,_=QFileDialog.getOpenFileName(self,"Open Image","","All Files(*.jpg *.png *.jpeg)",options=self.w)

            #Orginal Image Widget
            pixmap=QPixmap(fileName)
            pixmap2=pixmap.scaledToWidth(int(self.width/2))
            self.loadedImage.setPixmap(pixmap2)
            self.loadedImage.adjustSize()
            self.loadedImagePath=fileName

        self.w=None

    def save(self):
        try:
            #If path is empty, raise FileNotFoundError
            if(len(self.loadedImagePath)==0):
                raise FileNotFoundError 
            self.manipulatedImage.pixmap().save("SavedImage.jpg","JPG")
            self.message.setText("Image Saved Successfully!")
        #Display Error message
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

    def reverseColor(self):
        try:
            image=cv2.imread(self.loadedImagePath)

            if(image is None):
                raise FileNotFoundError
            

            image=(255-image)
            cv2.imwrite("temp.jpg",image)

            pixmap=QPixmap("./temp.jpg")
            pixmap2=pixmap.scaledToWidth(int(self.width/2))

            self.manipulatedImage.setPixmap(pixmap2)
            self.manipulatedImage.adjustSize()
            self.message.setText("")

        except FileNotFoundError:
            self.message.setText("You have to Load an Image before reversing color!")
        
        except Exception as E:
            self.message.setText(str(E))

    def grayScale(self):
        try:
            image=cv2.imread(self.loadedImagePath)
            if(image is None):
                raise FileNotFoundError
            gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            cv2.imwrite("temp.jpg",gray_image)

            pixmap=QPixmap("./temp.jpg")
            pixmap2=pixmap.scaledToWidth(int(self.width/2))

            self.manipulatedImage.setPixmap(pixmap2)
            self.manipulatedImage.adjustSize()

            self.message.setText("")

        #Display relevant error message!
        except FileNotFoundError:
            self.message.setText("You have to Load an Image before Gray Scaling!")
        except Exception as E:
            self.message.setText(str(E))
            print(E)

    def crop(self):
        if self.inputWindow is None:
            try:
                #self.inputWindow=QWidget()
                if(len(self.loadedImagePath)==0):
                    raise FileNotFoundError
                start,okPressed=QInputDialog.getText(self, "Get coordinates","Enter Starting Point (Top Left:)\n in format x,y \n for example 120,85",QLineEdit.Normal,"",)
                end,okPressed=QInputDialog.getText(self,"Get coordinates","Enter Ending Point (Bottom Right):\n in format x.y\n for example 120,85",QLineEdit.Normal,"")

                image=cv2.imread(self.loadedImagePath)
                if(image is None):
                    raise FileNotFoundError
                
                if(len(start.split(","))!=2 or len(end.split(","))!=2):
                    raise Exception
                
                image=np.array(image)

                #coordinates of starting point (top-left)
                x1=int (start.split(",")[0])
                y1=int(start.split(",")[1])

                #coordinates of end point (right-bottom)
                x2=int(end.split(",")[0])
                y2=int(end.split(",")[1])

                #crop image with inputs
                croppedImage=image[x1:x2,y1:y2]

                cv2.imwrite("temp.jpg",croppedImage)
                pixmap=QPixmap("./temp.jpg")
                pixmap2=pixmap.scaledToWidth(int(self.width/2))

                self.manipulatedImage.setPixmap(pixmap2)
                self.manipulatedImage.adjustSize()
            except FileNotFoundError:
                self.message.setText("You have to Load an Image befor Cropping!")
            except Exception as E:
                self.message.setText("Invalid Input, \n It can be a good idea to review pixel size of orginal image by giving inputs!")
                print(E)


    def flip(self):
        if (self.flipImage is None):
            try:
                flipValue,okPressed=QInputDialog.getText(self,"Rotation", "Enter value for your options\n" "0:Vertical Flip\n" "1:Horizontal Flip",QLineEdit.Normal,"",)

                image=cv2.imread(self.loadedImagePath)

                if(image is None):
                    raise FileNotFoundError
                elif int(flipValue)>1:
                    raise Exception
                
                #Second argiment of cv2.flip is horizontal or vertical
                #0 for vertical flip
                # 1 for horizontal flip

                flippedImage=cv2.flip(image,int(flipValue))
                cv2.imwrite("temp.jpg",flippedImage)

                pixmap=QPixmap("./temp.jpg")
                pixmap2=pixmap.scaledToWidth(int(self.width/2))

                self.manipulatedImage.setPixmap(pixmap2)
                self.manipulatedImage.adjustSize()
                self.message.setText("")

            #Display relevant error message
            except FileNotFoundError:
                self.message.setText("You have to Load an Image befor Flipping!")
            except Exception as E:

                self.message.setText("Invalid Input")
                print(E)

    def mirror(self):
        try:
            image=cv2.imread(self.loadedImagePath)
            if (image is None):
                raise FileNotFoundError
            
            mirroredImage=cv2.flip(image,1)
            cv2.imwrite("temp.jpg",mirroredImage)

            pixmap=QPixmap("./temp.jpg")
            pixmap2=pixmap.scaledToWidth(int(self.width/2))


            self.manipulatedImage.setPixmap(pixmap2)
            self.manipulatedImage.adjustSize()
            self.message.setText("")

        #Display relevant error
        except FileNotFoundError:
            self.message.setText("You have to Load an Image before mirroring!")
        except Exception as E:
            self.message.setText(str(E))
            print(E)

    def rotate(self):
        if self.inputWindowOfRotation is None:
            try:
                if(len(self.loadedImagePath)==0):
                    raise FileNotFoundError
            
                rotationDegree,okPressed=QInputDialog.getText(self,"Rotation","Enter the Rotation Degree", QLineEdit.Normal,"",)

                image=cv2.imread(self.loadedImagePath)
                rotatedImage=ndimage.rotate(image,int(rotationDegree))

                cv2.imwrite("temp.jpg",rotatedImage)

                pixmap=QPixmap("./temp.jpg")
                pixmap2=pixmap.scaledToWidth(int(self.width/2))

                self.manipulatedImage.setPixmap(pixmap2)
                self.manipulatedImage.adjustSize()
                self.message.setText("")
            
            #display relevant error message
            except FileNotFoundError:

                self.message.setText("You have to Load an Image before rotation!")

            except Exception as E:
                self.message.setText(str(E))
                print(E)

           


app=QApplication(sys.argv)
main=MainWindow()
main.show()
app.exec()

        
