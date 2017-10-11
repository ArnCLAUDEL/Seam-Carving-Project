import tkinter
from tkinter.filedialog import askopenfilename

class Frame:

    def __init__(self, frame, core):
        self.frame = frame
        self.core = core
        self.__initialize()
        

    def __initialize(self):
        self.frame.title("machinerie")
        
        self.load_button = tkinter.Button(self.frame, text="Load", command=self.load)
        self.load_button.pack()

        self.label = tkinter.StringVar()
        self.label.set("NONE")

        self.test_button = tkinter.Button(self.frame, text="Test", command=self.energyTest)
        self.test_button.pack()
        
        self.current_file_label = tkinter.Label(self.frame, textvariable=self.label)
        self.current_file_label.pack()

    def load(self):
        file = askopenfilename(title="Select a picture", filetypes=[("jpeg files", "*.jpg")])

        if file:
            print("Picture selected")
            self.core.setImage(file)
            print("Picture loaded")
            self.updateLabel()

    def updateLabel(self):
        self.label.set(self.core.image.path)

    def energyTest(self):
        self.core.energyOf(2,3)
