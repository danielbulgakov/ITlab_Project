import tkinter as tk
from PIL import Image, ImageTk

import serial.tools.list_ports


import MenuPages
import RTInfoPages

import AssetsClass.ConnectHandler as ConHan
ch = ConHan.ConnectHandler()


from AssetsClass.UsersData import WorkerUsersData
from AssetsClass.GlobalVariables import user_login


MyText = 'Arial 17 bold'
EntryText = "Arial 14 bold"
StyleText = "Arial 14 bold"


wud = WorkerUsersData() #объект того самого класса для работы с данными



class MainProfilePage(tk.Frame):

    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent, bg='white')

        self.img = tk.PhotoImage(file="Pictures\setting.png")
        self.img = self.img.subsample(10,10)
        self.btn_setting = tk.Button(self, bg='white', image=self.img, compound=tk.TOP, highlightthickness=0, bd=0, 
                                    padx=10, text="настройки", font=StyleText, command=lambda: control.show_frame(SettingPage))
        self.btn_setting.grid(row=0, column=0)

        self.img1 = tk.PhotoImage(file="Pictures\\avatar.png")
        self.img1 = self.img1.subsample(10,10)
        self.btn_profile = tk.Button(self, bg='white', image=self.img1, compound=tk.TOP, highlightthickness=0, bd=0,
                                    padx=25, text="мой профиль", font=StyleText, command=lambda: control.show_frame(ProfileDataPage))
        self.btn_profile.grid(row=0, column=2, sticky=tk.W)


        temp = Image.open("Pictures\medical_care.png")
        temp = temp.resize((62, 62), Image.ANTIALIAS)
        temp = ImageTk.PhotoImage(temp)
        self.btn_params = tk.Button(self, image=temp, compound=tk.TOP, highlightthickness=0, bd=0, 
                                    padx=200, text="здоровье", font=StyleText, pady=2, bg="green", activebackground="green", command=lambda: control.show_frame(RTInfoPages.HealthPage))
        self.btn_params.image=temp
        self.btn_params.grid(row=0, column=1)

        maintext = "\n\nЭто главная страница вашего профиля.\n\nЗдесь приведена небольшая инструкция по пользованию.\n\nПри нажатии первой слева кнопки вызывается окно, \nгде устанавливаются параметры для подключения к микроконтроллеру.\n\nПри нажатии второй слева кнопки вызывается окно, \nгде будут отображены ваши параметры.\n\nПри нажатии третьей кнопки слева вызывется окно, \nгде будут представлены данные профиля."
        self.label1 = tk.Label(self, bg='white', text=maintext, font=StyleText, justify=tk.CENTER).grid(row=1, column=0, columnspan=3)

        self.img2 = tk.PhotoImage(file="Pictures//back.png")
        self.img2 = self.img2.subsample(10,10)
        self.btn_back = tk.Button(self, bg='white', image=self.img2, compound=tk.TOP, highlightthickness=0, bd=0,
                                    padx=25, text="выйти", font=StyleText, command=lambda: [ control.show_frame(MenuPages.StartPage)])
        self.btn_back.grid(row=2, column=0, columnspan=3 ,sticky=tk.N)
    


class SettingPage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent, bg='white')

        self.img = tk.PhotoImage(file="Pictures\home_page_profile.png")
        self.img = self.img.subsample(10,10)
        self.btn_back = tk.Button(self, bg='white', image=self.img, compound=tk.TOP, highlightthickness=0, bd=0,
                                 padx=25, text="Домой", font=StyleText, command=lambda: control.show_frame(MainProfilePage))
        self.btn_back.grid(row=0, column=0)

        self.port_label = tk.Label(self, bg='white', text = "Available Port(s): ", font=StyleText)
        self.port_label.grid(column=1, row = 2, pady= 20, padx= 10) 


        self.port_bd = tk.Label(self, bg='white', text = "Baude Rate: ", font=StyleText)
        self.port_bd.grid(column=1, row = 3, pady= 20, padx= 10) 

        self.refresh_btn = tk.Button(self, text = "R", height= 2, width= 10, command=self.update_coms)
        self.refresh_btn.grid(column=3, row=2)

        self.connect_btn = tk.Button(self, text = "Подкл-ся", height= 2, width= 10, state="disabled", command=self.connection)
        self.connect_btn.grid(column=3, row=4)
        
        self.baud_select()
        self.update_coms()

    def connect_check(self,  arg):
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



    def connection(self):
        global ch
        if self.connect_btn["text"] in "Откл-ся":
            self.connect_btn["text"] = "Подкл-ся"
            self.refresh_btn["state"] = "active"
            self.drop_bd["state"] = "active"
            self.drop_COM["state"] = "active"
            self.serialData = False
            ch.enddata(False)
            ch.setconditionthread(False)
        else:
            self.serialData = True
            self.connect_btn["text"] = "Откл-ся"
            self.refresh_btn["state"] = "disable"
            self.drop_bd["state"] = "disable"
            self.drop_COM["state"] = "disable"
            self.port = self.clicked_com.get()
            self.baud = self.clicked_bd.get()
        
            try:
                #ser = serial.Serial(self.port, self.baud, timeout=0)
                 ch.connect(self.port, self.baud, self.serialData)
            except:
                pass

            if  ch.getconditionthread() is False:
                print("test is success")
                ch.createthread()
                ch.setconditionthread(True)
            else:
                pass

class ProfileDataPage(tk.Frame):

    def __init__(self, parent, control):

        tk.Frame.__init__(self,parent, bg='white')

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
        self.btn_back = tk.Button(self, bg='white', image=self.img, compound=tk.TOP, highlightthickness=0, bd=0,
                                 text="Домой", font=StyleText, command=lambda: [self.delete_data(), control.show_frame(MainProfilePage)])
        self.btn_back.grid(row=0, column=0,columnspan=3, sticky=tk.W)

        fields = ["Имя", "Фамилия", "Телефон", "Email", "Вес", "Рост", "Возраст"]
        arr = [self.name, self.surname, self.phone, self.email, self.weight, self.height, self.age]

        labels = [tk.Label(self, bg='white', text=f, font=StyleText) for f in fields]
        self.entries = [tk.Entry(self, bg='white',width=30, state='disabled', font=StyleText, textvariable=d) for d in arr]
        self.widgets = list(zip(labels, self.entries))

        #self.fill_start_data()    

        for i, (label, entry) in enumerate(self.widgets):
            label.grid(row=i+1, column=0, sticky=tk.E, padx=100,columnspan=2)
            entry.grid(row=i+1, column=3, padx=10, pady=5)

        self.login_btn = tk.Button(self, bg='white', text="Изменить данные", command=self.changedataprofile)
        self.clear_btn = tk.Button(self, bg='white', text="Сохранить данные", command=self.savedataprofile)
        self.refres = tk.Button(self, bg='white', text="Обновить", command=self.fill_start_data)
       
        self.login_btn.place(relx=0.3, rely=0.7)
        self.clear_btn.place(relx=0.5, rely=0.7)
        self.refres.place(relx=0.7, rely=0.7)
    
    #добавить сохранение в файл
    def delete_data(self):
        for entry in self.entries:
            entry.config(state="normal")
            entry.delete(0,tk.END)
            entry.config(state="disable")

    def fill_start_data(self):
        self.delete_data()
        wud.set_user_login(user_login)
        i = wud.find_data()
        if i != 0:
            ls = wud.get_download_data()
            j = 1
            for entry in self.entries:
                entry.config(state="normal")
                entry.insert(0, ls[j])
                entry.config(state="disable")
                j += 1
        else:
            pass

    def changedataprofile(self):
        wud.set_user_login(user_login)
        for entry in self.entries:
            entry.config(state="normal")
            
            
    def savedataprofile(self):
        #wud.printlogin()
        i = wud.find_data()
        if i == 0:
            wud.write_data_in_file(self.name.get(), self.surname.get(), self.phone.get(), self.email.get(), 
                                self.weight.get(), self.height.get(), self.age.get())
        else:
            wud.rewrite_data_in_file(self.name.get(), self.surname.get(), self.phone.get(), self.email.get(), 
                                self.weight.get(), self.height.get(), self.age.get(), i)
        for entry in self.entries:
            entry.config(state="disable")
        