import cv2
import tkinter as tk
from tkinter import filedialog

class VideoConverterGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Video Converter")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Create a button to select the input video file
        self.input_file_button = tk.Button(self.frame, text="Select Input Video", command=self.select_input_file)
        self.input_file_button.pack()

        # Create a button to select the output video file path
        self.output_path_button = tk.Button(self.frame, text="Select Output Path", command=self.select_output_path)
        self.output_path_button.pack()

        # Create a button to start the conversion process
        self.convert_button = tk.Button(self.frame, text="Convert Video", command=self.convert_video)
        self.convert_button.pack()

        # Initialize variables to store input file and output file path
        self.input_file_path = None
        self.output_file_path = None

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])

    def select_output_path(self):
        self.output_file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])

    def convert_video(self):
        # Check if both input and output paths are provided
        if self.input_file_path is None or self.output_file_path is None:
            return

        # Read input video file
        cap = cv2.VideoCapture(self.input_file_path)

        # Get input video codec and frame rate
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Get input video width and height
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create output video writer
        out = cv2.VideoWriter(self.output_file_path, fourcc, fps, (width, height))

        # Read and write video frames until end of file
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        # Release input and output video resources
        cap.release()
        out.release()

        # Display message after completion of video conversion
        tk.messagebox.showinfo("Video Conversion", "Video conversion completed successfully.")

# Create the main window and start the GUI
root = tk.Tk()
root.geometry('600x400')
app = VideoConverterGUI(root)
root.mainloop()
