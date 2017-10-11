import tkinter
import model.core as core
import gui.frame as frame

root = tkinter.Tk()
core = core.Core()
frame = frame.Frame(root, core)
