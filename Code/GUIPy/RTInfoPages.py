from audioop import avg
from datetime import datetime
import tkinter as tk
import ProfilePages

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from AssetsClass.Heart import HeartGif
from datetime import datetime
import AssetsClass.GlobalVariables as gb

import random


MyText = 'Arial 17 bold'
EntryText = "Arial 14 bold"
StyleText = "Arial 14 bold"

#Тут должны быть графики пульса, spo2, активность
class HealthPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent, bg='white')
        
        self.home = tk.PhotoImage(file="Pictures\home_page_profile.png")
        self.home = self.home.subsample(10,10)
        self.btn_back = tk.Button(self, bg='white', image=self.home, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Домой", font=StyleText, command=lambda:[control.show_frame(ProfilePages.MainProfilePage)])
        self.btn_back.grid(row=0, column=0)
        
        self.heart = tk.PhotoImage(file="Pictures\heart.png")
        self.heart = self.heart.subsample(10,10)
        self.btn_heart = tk.Button(self, bg='white', image=self.heart, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="BPM", font=StyleText, command=lambda: control.show_frame(HeartBeatPage))
        self.btn_heart.grid(row=0, column=1)
        
        self.spo2 = tk.PhotoImage(file="Pictures\spo2.png")
        self.spo2 = self.spo2.subsample(10,10)
        self.btn_spo2 = tk.Button(self, bg='white', image=self.spo2, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="SPO2", font=StyleText, command=lambda: control.show_frame(SPO2BeatPage))
        self.btn_spo2.grid(row=0, column=2)

class HeartBeatPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent, bg='white')
    
        
        self.heartbeat = []
        self.time = []
        self.avg = 0;
        self.fig = plt.figure(1, figsize=(10, 4), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, self)  
        
        self.home = tk.PhotoImage(file="Pictures\home_page_profile.png")
        self.home = self.home.subsample(10,10)
        self.btn_home = tk.Button(self, bg='white', image=self.home, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Домой", font=StyleText, command=lambda: control.show_frame(ProfilePages.MainProfilePage), anchor='nw')
        self.btn_home.grid(row=0, column=0, sticky='nw')
        
        self.back = tk.PhotoImage(file="Pictures\\back-.png")
        self.back = self.back.subsample(10,10)
        self.btn_back = tk.Button(self, bg='white', image=self.back, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Назад", font=StyleText, command=lambda: control.show_frame(HealthPage), anchor='nw')
        self.btn_back.grid(row=0, column=1,  sticky='nw')
        
    
        heart = HeartGif(self, row=0,col=99, width=100, height=100)
        self.after(0, heart.update, min(max(30, 190 - int(self.avg)), 190-60)  ) 
        self.after(0, self.getdata, 1000)
        
        self.usefuldata = 'Среднее сердцебиение : ' + str(self.avg)
        
        self.label = tk.Label(self, bg='white', text=self.usefuldata, font=MyText)
        self.label.grid(row=2, column=0, columnspan=3)
        
        self.label1 = tk.Label(self, bg='white', text='Активность : нету данных', font=MyText)
        self.label1.grid(row=3, column=0, columnspan=3)

    def filter(self,array, value):
        array = np.asarray(array)
        if (array.max() == 0): return 0;
        idx = (np.abs(array - value)).argmin()
        if array[idx] == 0 or array[idx] > 180: return 80
        array = array[array!=0 ]
        array = array[array < 200]
        array = array[array > 20]
        return array.mean() - 20;
        return array[idx]

    def getdata(self, timespan = 1000):

        self.t = ProfilePages.ch.GetPulse() 
 
        temp = ProfilePages.ch.GetTime()
        
        self.avg = np.average(self.heartbeat)
        if (self.avg != self.avg): 
            self.avg = 0
            
        self.usefuldata = 'Среднее сердцебиение : ' + str(int(self.avg))
        self.label.configure(text=self.usefuldata)
        self.label.update()
        
        value = gb.ph.next_predict()
        if (value == "NoneType") : str(' ')
        self.label1.configure(text='Активность : '  + value)
        self.label1.update()
        
        if (len(self.t) != 0) :
            # avgk = self.filter(self.t, 80)
            avgk = np.mean(self.t)
            self.heartbeat.append(int(avgk))
            self.time.append(datetime.now())

        self.fig.clear()

        if (len(self.heartbeat) > 25) :
            self.heartbeat.pop(0)
            self.time.pop(0)
        

        if (len(self.t) != 0):
            self.plot(self.heartbeat)
        self.after(timespan, self.getdata, 1000)
        
        
    def plot(self, beats_array) : 
        plt.figure(1)
        x = np.array(self.time)
        y = np.array(beats_array)
        
        plt.plot(x, y, color="red")
        plt.ylim(40,200)
        
        # plt.axes().get_xaxis().set_visible(False)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=100)

class SPO2BeatPage(tk.Frame):
    
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent, bg='white')
        
        self.heartbeat = []
        self.time = []
        self.avg = 0
        self.after(0, self.getdata, 1000)

        
        self.fig = plt.figure(0, figsize=(10, 4), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, self)  
        
        self.home = tk.PhotoImage(file="Pictures\home_page_profile.png")
        self.home = self.home.subsample(10,10)
        self.btn_home = tk.Button(self, bg='white', image=self.home, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Домой", font=StyleText, command=lambda: control.show_frame(ProfilePages.MainProfilePage), anchor='nw')
        self.btn_home.grid(row=0, column=0, sticky='nw')
        
        self.back = tk.PhotoImage(file="Pictures\\back-.png")
        self.back = self.back.subsample(10,10)
        self.btn_back = tk.Button(self, bg='white', image=self.back, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Назад", font=StyleText, command=lambda:[ control.show_frame(HealthPage)], anchor='nw')
        self.btn_back.grid(row=0, column=1,  sticky='nw')
        self.spo2 = tk.PhotoImage(file="Pictures\spo2.png")
        self.spo2 = self.spo2.subsample(10,10)
        self.btn_spo2 = tk.Button(self, bg='white', image=self.spo2, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, font=StyleText, command=lambda: control.show_frame(SPO2BeatPage))
        self.btn_spo2.grid(row=0, column=99)
        
        self.avg = np.average(self.heartbeat)
        if (self.avg != self.avg) : self.avg = 0
        
        self.usefuldata = 'Средняя оксигенация : ' + str(self.avg)
        
        self.label = tk.Label(self, bg='white', text=self.usefuldata, font=MyText)
        self.label.grid(row=2, column=0, columnspan=3)




    def filter(self,array, value):
        array = np.asarray(array)
        if (array.max() == -1): return 0;
        idx = (np.abs(array - value)).argmin()
        if array[idx] <= 90 : return 95
        return array[idx]

        
    def getdata(self, timespan):
      
        self.t = ProfilePages.ch.GetSpO2() 
        temp = ProfilePages.ch.GetTime()
        
        self.avg = np.average(self.heartbeat)
        if (self.avg != self.avg): 
            self.avg = 0
        self.usefuldata = 'Средняя оксигенация : ' + str('%.1f' % self.avg)
        self.label.configure(text=self.usefuldata)
        self.label.update()
        




        if (len(self.t) != 0) :
            # avgk = self.filter(self.t, 95)
            avgk = np.mean(self.t)
            self.heartbeat.append(int(avgk))
            self.time.append(datetime.now())

        self.fig.clear()


        if (len(self.heartbeat) > 25) :
            self.heartbeat.pop(0)
            self.time.pop(0)
        

        if (len(self.t) != 0):
            self.plot(self.heartbeat)
        self.after(timespan, self.getdata, 1000)
        
        
    def plot(self, beats_array) : 
        plt.figure(0)
        y = np.array(beats_array)
        x = np.array(self.time)
        
        plt.plot(x, y, color="blue")
        plt.ylim(0,100)
        
        # plt.axes().get_xaxis().set_visible(False)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        
        self.canvas.draw()
      
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=100)
