from os import stat
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from pyparsing import col
import serial.tools.list_ports
import threading


StyleText = "Arial 14 bold"

class Graphics():
    pass

class MainProfilePage(tk.Frame):

    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="GUI\Pictures\setting.png")
        self.img = self.img.subsample(10,10)
        self.btn_setting = tk.Button(self, image=self.img, compound=tk.TOP, highlightthickness=0, bd=0, 
                                 padx=10, text="настройки", font=StyleText, command=lambda: control.show_frame(SettingPage))
        self.btn_setting.grid(row=0, column=0)

        self.img1 = tk.PhotoImage(file="GUI\Pictures//avatar.png")
        self.img1 = self.img1.subsample(10,10)
        self.btn_profile = tk.Button(self, image=self.img1, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="мой профиль", font=StyleText, command=lambda: control.show_frame(ProfileDataPage))
        self.btn_profile.grid(row=0, column=2, sticky=tk.W)


        temp = Image.open("GUI\Pictures\medical_care.png")
        temp = temp.resize((62, 62), Image.ANTIALIAS)
        temp = ImageTk.PhotoImage(temp)
        self.btn_params = tk.Button(self, image=temp, compound=tk.TOP, highlightthickness=0, bd=0, 
                                 padx=200, text="здоровье", font=StyleText, pady=2, bg="green", activebackground="green", command=lambda: control.show_frame(HealthPage))
        self.btn_params.image=temp
        self.btn_params.grid(row=0, column=1)

        maintext = "\n\nЭто главная страница вашего профиля.\n\nЗдесь приведена небольшая инструкция по пользованию.\n\nПри нажатии первой слева кнопки вызывается окно, \nгде устанавливаются параметры для подключения к микроконтроллеру.\n\nПри нажатии второй слева кнопки вызывается окно, \nгде будут отображены ваши параметры.\n\nПри нажатии третьей кнопки слева вызывется окно, \nгде будут представлены данные профиля."
        self.label1 = tk.Label(self, text=maintext, font=StyleText, justify=tk.CENTER).grid(row=1, column=0, columnspan=3)
        
        self.img2 = tk.PhotoImage(file="GUI\Pictures//back.png")
        self.img2 = self.img2.subsample(10,10)
        self.btn_back = tk.Button(self, image=self.img2, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="выйти", font=StyleText, command=lambda: control.show_frame(ProfileDataPage))
        self.btn_back.grid(row=2, column=0, columnspan=3 ,sticky=tk.N)


class SettingPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="GUI\Pictures\home_page_profile.png")
        self.img = self.img.subsample(10,10)
        self.btn_back = tk.Button(self, image=self.img, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="home", font=StyleText, command=lambda: control.show_frame(MainProfilePage))
        self.btn_back.grid(row=0, column=0)

        self.port_label = tk.Label(self, text = "Available Port(s): ", font=StyleText)
        self.port_label.grid(column=1, row = 2, pady= 20, padx= 10) 


        self.port_bd = tk.Label(self, text = "Baude Rate: ", font=StyleText)
        self.port_bd.grid(column=1, row = 3, pady= 20, padx= 10) 

        self.refresh_btn = tk.Button(self, text = "R", height= 2, width= 10, command=self.update_coms)
        self.refresh_btn.grid(column=3, row=2)

        self.connect_btn = tk.Button(self, text = "Connect", height= 2, width= 10, state="disabled", command=self.connection)
        self.connect_btn.grid(column=3, row=4)
        
        self.baud_select()
        self.update_coms()

    def connect_check(self,arg):
        if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
            self.connect_btn["state"] = "disable"
        else:
            self.connect_btn["state"] = "active"

    def baud_select(self):
        self.clicked_bd = tk.StringVar()
        bds = ["-", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "56000", "57600", "115200", "128000", "256000"]
        self.clicked_bd.set(bds[0])
        self.drop_bd = tk.OptionMenu(self, self.clicked_bd, *bds, command=self.connect_check)
        self.drop_bd.config(width= 20)
        self.drop_bd.grid(column=2, row=3, padx=50)

    def update_coms(self):
        self.ports = serial.tools.list_ports.comports()
        #print(ports)
        coms = [com[0] for com in self.ports]
        #print(coms)
        coms.insert(0,"-")
        try:
            self.drop_COM.destroy()
        except:
            pass
        self.clicked_com = tk.StringVar()
        self.clicked_com.set(coms[0])
        self.drop_COM = tk.OptionMenu(self, self.clicked_com, *coms, command=self.connect_check)
        self.drop_COM.config(width= 20)
        self.drop_COM.grid(column=2, row=2, padx=50)
        self.connect_check(0)

    def readSerial(self):
        #print("thread start")
        self.serialData
        while self.serialData:
            #Получается массив байт
            data = ser.readline()
            if len(data) > 0:
                try:
                    data1 = str(data, 'utf-8')
                    #sensor = int(data.decode('utf8'))
                    print(data1)
                except:
                    pass

    def connection(self):
        global ser
        if self.connect_btn["text"] in "Disconnect":
            self.connect_btn["text"] = "Connect"
            self.refresh_btn["state"] = "active"
            self.drop_bd["state"] = "active"
            self.drop_COM["state"] = "active"
            self.serialData = False
        else:
            self.serialData = True
            self.connect_btn["text"] = "Disconnect"
            self.refresh_btn["state"] = "disable"
            self.drop_bd["state"] = "disable"
            self.drop_COM["state"] = "disable"
            self.port = self.clicked_com.get()
            self.baud = self.clicked_bd.get()
            try:
                ser = serial.Serial(self.port, self.baud, timeout=0)
            except:
                pass
            t1 = threading.Thread(target= self.readSerial)
            t1.daemon = True
            t1.start()

#Тут должны быть графики пульса, spo2, активность
class HealthPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="GUI\Pictures\home_page_profile.png")
        self.img = self.img.subsample(10,10)
        self.btn_back = tk.Button(self, image=self.img, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="home", font=StyleText, command=lambda: control.show_frame(MainProfilePage))
        self.btn_back.grid(row=0, column=0)

        


class ProfileDataPage(tk.Frame):

    def __init__(self, parent, control):

        tk.Frame.__init__(self,parent)

        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.weight = tk.StringVar()
        self.height = tk.StringVar()
        self.age = tk.StringVar()

        self.contr = False

        self.img = tk.PhotoImage(file="GUI\Pictures\home_page_profile.png")
        self.img = self.img.subsample(10,10)
        self.btn_back = tk.Button(self, image=self.img, compound=tk.TOP, highlightthickness=0, bd=0,
                                 text="home", font=StyleText, command=lambda: control.show_frame(MainProfilePage))
        self.btn_back.grid(row=0, column=0,columnspan=3, sticky=tk.W)


        fields = ["Имя", "Фамилия", "Телефон", "Email", "Вес", "Рост", "Возраст"]
        labels = [tk.Label(self, text=f, font=StyleText) for f in fields]
        self.entries = [tk.Entry(self,width=30, state='disabled', font=StyleText) for _ in fields]
        self.widgets = list(zip(labels, self.entries))
            

        for i, (label, entry) in enumerate(self.widgets):
            label.grid(row=i+1, column=0, sticky=tk.E, padx=100,columnspan=2)
            entry.grid(row=i+1, column=3, padx=10, pady=5)
      

        self.login_btn = tk.Button(self, text="Изменить данные", command=self.changedataprofile)
        self.clear_btn = tk.Button(self, text="Сохранить данные", command=self.savedataprofile)
       
        self.login_btn.place(relx=0.3, rely=0.7)
        self.clear_btn.place(relx=0.5, rely=0.7)
    
    #добавить сохранение в файл

    def changedataprofile(self):
        for entry in self.entries:
            entry.config(state="normal")
            
            
    def savedataprofile(self):
        for entry in self.entries:
            entry.config(state="disable")
        