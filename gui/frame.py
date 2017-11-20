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

        self.test_button = tkinter.Button(self.frame, text="Test", command=self.test)
        self.test_button.pack()

        self.refresh_button = tkinter.Button(self.frame, text="Refresh", command=self.update)
        self.refresh_button.pack()
                
        self.test_canvas = tkinter.Canvas(self.frame, width=1200, height=600)
        self.test_canvas.pack()
        
        self.current_file_label = tkinter.Label(self.frame, textvariable=self.label)
        self.current_file_label.pack()

        self.core.setImage("resources/pictures/ski.jpg")
        self.update()

        self.test()
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
        self.test_canvas.create_image(0,0, image=self.current_image, anchor ="nw")

    def test(self):
        #print(self.core.image.grid)
        #print(self.core.image.grid[0])
        for i in range(0,5):
            pl = self.core.stupid_seam_finder()

            for p in pl["path"]:
                self.test_canvas.create_oval(p[0]-0.5,p[1]-0.5,p[0]+0.5,p[1]+0.5)

            self.core.removeVerticalSeam(pl["path"])
        #self.update()
        
