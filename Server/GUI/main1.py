import tkinter as tk
from typing import Text
from menu_pages import WelcomePage, StartPage, EntryPage, RegisterPage
from profile import MainProfilePage, SettingPage, ProfileDataPage, HealthPage


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ESPушка")
        self.geometry("800x600")
        self.iconbitmap("GUI\Pictures\ESP32.ico") #D:\Programming_YuninDD\ITlab_Project\Server\GUI\Pictures\ESP32.ico


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        self.frames = {}
        for F in (WelcomePage, StartPage, EntryPage, RegisterPage, MainProfilePage, SettingPage, ProfileDataPage, HealthPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainProfilePage)
        

    def run(self):
        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()





if __name__ == "__main__":
    window = MainWindow()
    window.run()
