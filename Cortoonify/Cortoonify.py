import cv2 #importing Opencv Library
import numpy as np #importing Numpy
import tkinter as tk #Tkinter Python Gui library
from tkinter import filedialog #importing Thinter filedialog field

class CartoonifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cartoonify Image")
        
        # Create a menu bar 
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        # Create a canvas to display the image /간와스를 만들기 사진이 화면 출력을 위해
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        
        # Create a button to cartoonify the image / 사진을 만화로 반한하는 버튼 만들기
        cartoonify_button = tk.Button(root, text="Cartoonify", command=self.cartoonify_image)
        cartoonify_button.pack()
        
        # Create a variable to store the path of the selected file /선택한 파일을 저장하기 위한 번수
        self.filepath = None
        
    def open_file(self):
        self.filepath = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if self.filepath:
            # Read the image from file and display it on the canvas /선택한 사진을 읽고 화면에 출력
            img = cv2.imread(self.filepath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (400, 400))
            self.photo = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    
    def cartoonify_image(self):
        if self.filepath:
            # Read the image from file and convert it to a cartoon-like image / 선택한 사진을 읽고 만화로 변경시키기
            img = cv2.imread(self.filepath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
            cartoon = cv2.resize(cartoon, (400, 400))
            self.photo = tk.PhotoImage(data=cv2.imencode('.png', cartoon)[1].tobytes())
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

## Print Result
root = tk.Tk()
app = CartoonifyApp(root)
root.mainloop()
