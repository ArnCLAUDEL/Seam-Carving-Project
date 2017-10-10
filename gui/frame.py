from tkinter import *
from tkinter.filedialog import askopenfilename

class Frame:

    def __init__(self, frame, core):
        self.frame = frame
        self.core = core
        self.__initialize()
        

    def __initialize(self):
        self.frame.title("machinerie")
        
        self.load_button = Button(self.frame, text="Load", command=self.load)
        self.load_button.pack()
        

    def load(self):
        file = askopenfilename(title="Select a picture", filetypes=[("jpeg files", "*.jpg")])

        if file:
            print("File selected")
            core.setFile(file)

root = Tk()
frame = Frame(root)
root.mainloop()
