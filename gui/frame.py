from tkinter import *
from tkinter.filedialog import askopenfilename

class Frame:

    def __init__(self, frame):
        self.frame = frame
        self.initialize()
        

    def initialize(self):
        self.frame.title("machinerie")
        
        self.load_button = Button(self.frame, text="Load", command=self.load)
        self.load_button.pack()
        

    def load(self):
        file = askopenfilename(title="Select a picture", filetypes=[("jpeg files", "*.jpg")])

        if file:
            print(file)

root = Tk()
frame = Frame(root)
root.mainloop()
