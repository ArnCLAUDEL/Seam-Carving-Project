import tkinter
import model.core as core
import gui.frame as frame
import sys

sys.setcheckinterval(0)
root = tkinter.Tk()
core = core.Core()
frame = frame.Frame(root, core)
