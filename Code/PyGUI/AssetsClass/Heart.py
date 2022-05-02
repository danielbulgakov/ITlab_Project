from tkinter import *
from PIL import ImageTk,Image

class HeartGif:
    
    def __init__(self, root, posx=0, posy=0, width=500, height=500):
        self.frameCnt = 10
        self.frames = [ImageTk.PhotoImage(Image.open('Heart/heart (' + str(i) + ').png').resize((width, height),Image.ANTIALIAS)) for i  in range(1, self.frameCnt + 1)]
        self.posx = posx
        self.posy = posy
        self.height = height
        self.width = width
        self.root = root
        self.label =  Label(root)
        self.label.pack()
        self.isPos = True
        self.isRel = False
        self.ind = 0
    
    def __init__(self, root, relx=0, rely=0, width=500, height=500):
        self.frameCnt = 10
        self.frames = [ImageTk.PhotoImage(Image.open('Heart/heart (' + str(i) + ').png').resize((width, height),Image.ANTIALIAS)) for i  in range(1, self.frameCnt + 1)]
        self.relx = relx
        self.rely = rely
        self.height = height
        self.width = width
        self.root = root
        self.label =  Label(root)
        self.label.place(relx=relx, rely=rely)
        self.isRel = True
        self.isPos = False
        self.ind = 0
    
    def update(self, speed):
        self.ind += 1
        if self.ind == self.frameCnt:
            self.ind = 0
    
        self.label.configure(image= (self.frames[self.ind]))
        self.root.after(speed, self.update, speed)
        
        if (self.isPos): self.label.pack()
        elif(self.isRel) : self.label.place(relx=self.relx, rely=self.rely)
    
        
    # How to use
# heart = HeartGif(root, relx=0.3, rely=0.3, width=300, height=300)
# root.after(0, heart.update, 50)

