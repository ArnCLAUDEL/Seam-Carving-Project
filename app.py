import tkinter
import model.core as core
import gui.frame as frame
import sys

sys.setcheckinterval(0)
core = core.Core()
frame = frame.Frame(core)
