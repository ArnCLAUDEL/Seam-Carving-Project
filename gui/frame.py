import model.image as img
import numpy
import tkinter

from model.seamCarvingUtil import *
from tkinter.filedialog import askopenfilename

class Frame:

    def __init__(self,  core):
        self.frame = tkinter.Tk()
        self.core = core
        self.current_image = None
        self.__initialize()

    def __initialize(self):
        self.frame.title("Seam Carver")

        # # StringVars

        # StringVar with image information
        self.image_information = tkinter.StringVar()
        self.image_information.set("NONE")

        # StringVar with a message for the user
        self.user_message= tkinter.StringVar()
        self.user_message.set("Load an image to start.")

        # # Buttons

        # Button used to load a new image
        self.load_button = tkinter.Button(self.frame, text="Load", command=self.load)
        self.load_button.pack()

        # Frame that will contain buttons for resizing
        self.resize_buttons = tkinter.Frame(self.frame)
        self.resize_buttons.pack()

        # Button used to reduce the width by 1px
        self.reduce_width = tkinter.Button(self.resize_buttons, text="-", command=lambda: self.resize_image_width(-1))
        self.reduce_width.pack(side="left")

        # Button used to reduce automatically the image by 100px
        self.auto_find = tkinter.Button(self.resize_buttons, text="auto", command=lambda: self.auto_finder(100))
        self.auto_find.pack(side="left")

        # Button used to increase the width by 1px
        self.increase_width = tkinter.Button(self.resize_buttons, text="+", command=lambda: self.resize_image_width(1))
        self.increase_width.pack(side="left");

        # Button used to refresh the image
        self.refresh_button = tkinter.Button(self.frame, text="Refresh", command=self.update)
        self.refresh_button.pack()

        # # Canvas

        # Canvas that will contain the image
        self.canvas = tkinter.Canvas(self.frame, width=100, height=100, highlightthickness=0)
        self.canvas .pack(expand=1)

        # Callback when the size of the windows changes
        self.canvas.bind("<Configure>", self.on_resize)

        # # Labels

        # Label that displays a message to the user
        self.user_message_label = tkinter.Label(self.frame, textvariable=self.user_message)
        self.user_message_label.pack()

        # Label that displays image information
        self.image_information_label = tkinter.Label(self.frame, textvariable=self.image_information)
        #self.image_information_label.pack()

        self.frame.mainloop()

    # Displays a window to select a jpg image
    def load(self):
        file = askopenfilename(title="Select a picture", filetypes=[("jpeg files", "*.jpg")])

        if file:
            self.user_message.set("We are pre-processing your image")
            self.frame.update()
            self.core.set_image(file)
            self.user_message.set("")
            self.update()
        else:
            self.user_message.set("Load an image to start.")

    # Update the frame, the image and its information
    def update(self):
        # Image path + size
        self.image_information.set(self.core.image.path + " " + str(self.core.w()) + "x" + str(self.core.h()))
        self.current_image = self.core.get_image()

        # The minimum size is restricted by the size of the image
        self.frame.minsize(self.core.w()-1,self.core.h()+200-1)

        # We adjust the size of the canvas to the image
        self.canvas.configure(width=self.core.w(), height=self.core.h())

        # This draws the image on the canvas
        self.canvas.create_image(0, 0, image=self.current_image, anchor="nw")

    # Callback that allows the user to resize the image by resizing the windows
    @timer
    def on_resize(self, event):
        if self.core.w() != False and self.canvas.winfo_width() < self.core.w():
            pl = self.core.stupid_seam_finder(b=False)
            self.core.remove_vertical_seam(pl["path"])
            self.update()
            for p in pl["path"]:
                self.canvas .create_oval(p[0] - 0.5, p[1] - 0.5, p[0] + 0.5, p[1] + 0.5)

    def auto_finder(self, value):
        for i in range(value):
            self.resize_image_width(-1)
            self.frame.update()

    # Resize the image with the given value
    def resize_image_width(self, value):
        self.canvas.configure(width=self.canvas.winfo_width() + value)