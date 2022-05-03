from glob import glob
import tkinter as tk
from PIL import Image, ImageTk
import serial.tools.list_ports
import threading
import menu_pages
import struct as strct



StyleText = "Arial 14 bold"

class CollectorData():
    def __init__(self):
        pass

class Graphics():
    pass

class MainProfilePage(tk.Frame):

    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="Pictures\setting.png")
        self.img = self.img.subsample(10,10)
        self.btn_setting = tk.Button(self, image=self.img, compound=tk.TOP, highlightthickness=0, bd=0, 
                                 padx=10, text="настройки", font=StyleText, command=lambda: control.show_frame(SettingPage))
        self.btn_setting.grid(row=0, column=0)

        self.img1 = tk.PhotoImage(file="Pictures//avatar.png")
        self.img1 = self.img1.subsample(10,10)
        self.btn_profile = tk.Button(self, image=self.img1, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="мой профиль", font=StyleText, command=lambda: control.show_frame(ProfileDataPage))
        self.btn_profile.grid(row=0, column=2, sticky=tk.W)


        temp = Image.open("Pictures\medical_care.png")
        temp = temp.resize((62, 62), Image.ANTIALIAS)
        temp = ImageTk.PhotoImage(temp)
        self.btn_params = tk.Button(self, image=temp, compound=tk.TOP, highlightthickness=0, bd=0, 
                                 padx=200, text="здоровье", font=StyleText, pady=2, bg="green", activebackground="green", command=lambda: control.show_frame(HealthPage))
        self.btn_params.image=temp
        self.btn_params.grid(row=0, column=1)

        maintext = "\n\nЭто главная страница вашего профиля.\n\nЗдесь приведена небольшая инструкция по пользованию.\n\nПри нажатии первой слева кнопки вызывается окно, \nгде устанавливаются параметры для подключения к микроконтроллеру.\n\nПри нажатии второй слева кнопки вызывается окно, \nгде будут отображены ваши параметры.\n\nПри нажатии третьей кнопки слева вызывется окно, \nгде будут представлены данные профиля."
        self.label1 = tk.Label(self, text=maintext, font=StyleText, justify=tk.CENTER).grid(row=1, column=0, columnspan=3)
        
        self.img2 = tk.PhotoImage(file="Pictures//back.png")
        self.img2 = self.img2.subsample(10,10)
        self.btn_back = tk.Button(self, image=self.img2, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="выйти", font=StyleText, command=lambda: control.show_frame(menu_pages.StartPage))
        self.btn_back.grid(row=2, column=0, columnspan=3 ,sticky=tk.N)

#Тот класс откуда берутся все данные
class SettingPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="Pictures\home_page_profile.png")
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

        #те самые массивы данных
        self.ax = [] 
        self.ay = [] 
        self.az = []
        self.gx = [] 
        self.gy = [] 
        self.gz = []
        self.pulse = [] 
        self.sp02 = [] 
        self.time = [] 

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


    #Не придумал как очищать буфер
    def readSerial(self):
        #print("thread start")
        self.serialData
        while self.serialData:
            #Получается массив байт (несколько массивов байт ибо лучше не придумал как эту хрень сделать)
            data1 = self.ser.read(11)
            data2 = self.ser.read(240)
            data3 = self.ser.read(10)
            data4 = self.ser.read(40)
            data5 = self.ser.read(7)
            data6 = self.ser.read(10)
            if len(data1) > 0:
                try:
                    #Перенос этих всяких данных в нормальные форматы
                    check1 = strct.unpack('11c', data1)
                    print(check1)
                    #показания гиро и акса
                    check2 = strct.unpack('60f', data2)
                    print(check2)
                    #pulse
                    check3 = strct.unpack('10B', data3)
                    print(check3)
                    #spo2
                    check4 = strct.unpack('10f', data4)
                    print(check4)
                    #время
                    check5 = strct.unpack('7B', data5)
                    print(check5)
                    check6 = strct.unpack('10c', data6)
                    print(check6)
                    #заполнение массивов
                    for i in range(0, 10):
                        self.ax.append(check2[i])
                        
                    for i in range(10, 20):
                        self.ay.append(check2[i])
                        

                    for i in range(20, 30):
                        self.az.append(check2[i])
                        

                    for i in range(30, 40):
                        self.gx.append(check2[i])
                    
                    for i in range(40, 50):
                        self.gy.append(check2[i])
                       

                    for i in range(50, 60):
                        self.gz.append(check2[i])
                        

                    for i in range(0, 10):
                        self.pulse.append(check3[i])
                        

                    for i in range(0, 10):
                        self.sp02.append(check4[i])
                        

                    for i in range(0, 7):
                        self.time.append(check5[i])

                    print("АксX:")    
                    print(self.ax)
                    print("АксY:")    
                    print(self.ay)
                    print("АксZ:")    
                    print(self.az)
                    print("ГироX:")    
                    print(self.gx)
                    print("ГироY:")    
                    print(self.gy)
                    print("ГироZ:")    
                    print(self.gz)
                    print("Пульс:")    
                    print(self.pulse)
                    print("Кислород:")    
                    print(self.sp02)
                    print("Время:")    
                    print(self.time)
                    
                    self.ax.clear()
                    self.ay.clear()
                    self.az.clear()
                    self.gx.clear()
                    self.gy.clear()
                    self.gz.clear()
                    self.pulse.clear()
                    self.sp02.clear()
                    self.time.clear()


                    self.zzzzzzzz = self.ax
                    self.ax = self.zzzzzzzz
                    self.zzzzzzzz = self.ax
                    self.ax = self.zzzzzzzz
                    self.zzzzzzzz = self.ax
                    self.ax = self.zzzzzzzz
                    self.zzzzzzzz = self.ax
                    self.ax = self.zzzzzzzz
                except:
                    pass
        
           
    def getax(self):
        return self.ax

    def connection(self):
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
                self.ser = serial.Serial(self.port, self.baud)
            except:
                pass
            t1 = threading.Thread(target= self.readSerial)
            t1.daemon = True
            t1.start()

#Тот класс куда должны быть переданы эти данные
#Тут должны быть графики пульса, spo2, активность
class HealthPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.img = tk.PhotoImage(file="Pictures\home_page_profile.png")
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

        self.img = tk.PhotoImage(file="Pictures\home_page_profile.png")
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
        