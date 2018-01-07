import tkinter
import time
import numpy
from tkinter.filedialog import askopenfilename

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print(f, "done in", round((end - start), 2), "s")
        return res
    return f_timer


class Frame:

    def __init__(self,  core):
        self.frame = tkinter.Tk()
        self.core = core
        self.__initialize()
        

    def __initialize(self):
        self.frame.title("Seam Carver")
        
        self.load_button = tkinter.Button(self.frame, text="Load", command=self.load)
        self.load_button.pack()

        self.label = tkinter.StringVar()
        self.label.set("NONE")

        self.test_button = tkinter.Button(self.frame, text="Find Seam", command=self.test)
        self.test_button.pack()

        self.refresh_button = tkinter.Button(self.frame, text="Refresh", command=self.update)
        self.refresh_button.pack()
                
        self.test_canvas = tkinter.Canvas(self.frame, width=1200, height=1200, highlightthickness=0)
        self.test_canvas.pack(expand=1)
        
        self.current_file_label = tkinter.Label(self.frame, textvariable=self.label)
        self.current_file_label.pack()

        self.core.setImage("resources/pictures/ski.jpg")

        self.test_canvas.bind("<Configure>", self.on_resize)
        self.frame.mainloop()


    def load(self):
        file = askopenfilename(title="Select a picture", filetypes=[("jpeg files", "*.jpg")])

        if file:
            print("Picture selected")
            self.core.setImage(file)
            print("Picture loaded")
            self.update()

    def update(self):
        self.label.set(self.core.image.path + " " + str(self.core.w()) + "x" + str(self.core.h()))
        self.current_image = self.core.getImage()
        self.frame.minsize(self.core.w()-1,self.core.h()+200-1)
        self.test_canvas.configure(width=self.core.w(), height=self.core.h())
        self.test_canvas.create_image(0, 0, image=self.current_image, anchor="nw")

    @timer
    def on_resize(self, event):
        if self.core.w() != False and self.test_canvas.winfo_width() < self.core.w():
            pl = self.core.stupid_seam_finder(b=False)
            self.core.removeVerticalSeam(pl["path"])
            self.update()
            for p in pl["path"]:
                self.test_canvas.create_oval(p[0] - 0.5, p[1] - 0.5, p[0] + 0.5, p[1] + 0.5)

    @timer
    def test(self):
        for i in range(0,0):
            pl = self.core.stupid_seam_finder()

            for p in pl["path"]:
                self.test_canvas.create_oval(p[0]-0.5,p[1]-0.5,p[0]+0.5,p[1]+0.5)

            self.core.removeHorizontalSeam(pl["path"])

        for i in range(0,1):
            pl = self.core.stupid_seam_finder(b=False)

            for p in pl["path"]:
                self.test_canvas.create_oval(p[0] - 0.5, p[1] - 0.5, p[0] + 0.5, p[1] + 0.5)
            self.core.removeVerticalSeam(pl["path"])
