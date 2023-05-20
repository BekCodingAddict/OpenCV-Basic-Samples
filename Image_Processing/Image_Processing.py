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
        self.message.setGeometry(920,60,700,200)
        self.message.setStyleSheet("color:red; border:1px solid black; border-radius:8px;")


        #Set coordinate and size of main screen of application
        self.setGeometry(0,0,self.width,self.height)
        self.setWindowTitle("Final Term OpenCv Image Processing Project")


app=QApplication(sys.argv)
main=MainWindow()
main.show()
app.exec()

        
