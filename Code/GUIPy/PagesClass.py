from logging import Handler
import tkinter as tk
from typing import Text
from MenuPages import WelcomePage, StartPage, EntryPage, RegisterPage
from ProfilePages import MainProfilePage, SettingPage, ProfileDataPage
from RTInfoPages import  SPO2BeatPage, HeartBeatPage, HealthPage

        

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("ESPушка")
        self.geometry("800x600")
        self.iconbitmap("Pictures\ESP32.ico") #D:\Programming_YuninDD\ITlab_Project\Server\GUI\Pictures\ESP32.ico
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        self.frames = {}
        for F in (WelcomePage, StartPage, EntryPage, RegisterPage, MainProfilePage, SettingPage, ProfileDataPage, HealthPage, HeartBeatPage, SPO2BeatPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)
        
   
    def run(self):
        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()





if __name__ == "__main__":
    window = MainWindow()
    
    window.run()
