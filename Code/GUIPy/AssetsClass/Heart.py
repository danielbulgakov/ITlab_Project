from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import ProfilePages

class HeartGif:
    
    def __init__(self, root, row, col, width=500, height=500):
        self.frameCnt = 10
        self.frames = [ImageTk.PhotoImage(Image.open('AssetsClass\Heart/heart (' + str(i) + ').png').resize((width, height),Image.ANTIALIAS)) for i  in range(1, self.frameCnt + 1)]
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.root = root
        self.label =  Label(root, bg='white')
        self.label.grid(row=self.row, column=self.col, sticky='ne')
        self.ind = 0
        
    
    def update(self, speed):
        self.ind += 1
        if self.ind == self.frameCnt:
            self.ind = 0
    
        self.label.configure(image= (self.frames[self.ind]))
        self.label.update()

        self.root.after(speed, self.update,  min(max(30, 170 - int(np.average(ProfilePages.ch.GetPulse()))), 170-60))
        
    
        
    # How to use
# heart = HeartGif(root, relx=0.3, rely=0.3, width=300, height=300)
# root.after(0, heart.update, 50)

