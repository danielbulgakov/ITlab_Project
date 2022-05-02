import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from profile import MainProfilePage


MyText = 'Arial 17 bold'
EntryText = "Arial 14 bold"



class WelcomePage(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="Добро пожаловать в приложение!", font=MyText)
        label.place(relx=0.5, rely=0.2, anchor="center")

        my_image = tk.PhotoImage(file="GUI/Pictures/ESP_pictures.png")
        label1 = tk.Label(self, image=my_image)
        label1.image = my_image
        label1.place(relx=0.5, rely=0.7, anchor="center")

        login_button = tk.Button(self, text="В меню авторизации", height="2", width="25",font=MyText, fg="red",command=lambda: control.show_frame(StartPage))
        login_button.place(relx=0.5, rely=0.35, anchor="center" )

class StartPage(tk.Frame):

    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Выберите способ авторизации", font=MyText)
        label.place(relx=0.5, rely=0.3, anchor="center")
            
        login_button = tk.Button(self, text="Войти", height="2", width="30",font=MyText, command=lambda: control.show_frame(EntryPage))
        login_button.place(relx=0.5, rely=0.5, anchor="center" )
            
        signin_button = tk.Button(self ,text="Зарегистрироваться", height="2", width="30",font=MyText , command=lambda: control.show_frame(RegisterPage))
        signin_button.place(relx=0.5, rely=0.7, anchor="center")

class EntryPage(tk.Frame):

    def __init__(self, parent, control):
        tk.Frame.__init__(self,parent)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.control = control

        img = Image.open("GUI\Pictures\login.png")
        img = img.resize((25, 25), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image=img)
        panel.image = img
        panel.place(relx=0.25, rely=0.5, anchor="center")

        img1 = Image.open("GUI\Pictures\zamok.png")
        img1 = img1.resize((25, 25), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        panel1 = tk.Label(self, image=img1)
        panel1.image = img1
        panel1.place(relx=0.25, rely=0.6, anchor="center")

        label = tk.Label(self, text="Войдите в аккаунт", font=MyText)
        label.place(relx=0.5, rely=0.3, anchor="center")

        username_entry = tk.Entry(self, textvariable=self.username, font=EntryText, width=30)
        username_entry.place(relx=0.5, rely=0.5, anchor="center")
        
        password_entry = tk.Entry(self, textvariable=self.password, show="*", font=EntryText, width=30)
        password_entry.place(relx=0.5, rely=0.6, anchor="center")

        button_register = tk.Button(self, text="Вход", font=MyText, command=lambda: [self.check_register_data()])
        button_register.place(relx=0.4, rely=0.8, anchor="center")

        button_back = tk.Button(self, text="Назад", font=MyText, command=lambda: control.show_frame(StartPage))
        button_back.place(relx=0.6, rely=0.8, anchor="center")

    def check_register_data(self):
        name = str(self.username.get()).strip()
        password = str(self.password.get()).strip()

        if name.isspace() or password.isspace() or ' ' in name or ' ' in password or len(name) == 0 or len(password) == 0:   
            messagebox.showwarning(title='ошибка', message='неверно указаны данные')
        else :
            if self.find_register_data() :
                self.control.show_frame(MainProfilePage)
            else : 
                messagebox.showwarning(title='ошибка', message='неверно логин или пароль')
            
        
        self.username.set("")
        self.password.set("")
        
    def find_register_data(self):
        data = open("GUI\profiles.txt", "r")
        if (self.username.get() + "|" + self.password.get() + "\n") in data : 
            data.close()
            return True
        data.close()
        return False

class RegisterPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.rpassword = tk.StringVar()
        self.ctrl = controller
                
        
        label = tk.Label(self, text="Создание аккаунта", font=MyText)
        label.place(relx=0.5, rely=0.4, anchor="center")
        
        
        username_lable = tk.Label(self, text="Придумайте Логин * ", font=MyText)
        username_lable.place(relx=0.2, rely=0.5, anchor="center")
     
        
        username_entry = tk.Entry(self, textvariable=self.username, font=EntryText)
        username_entry.place(relx=0.6, rely=0.5, anchor="center")
        
        password_lable = tk.Label(self, text="Придумайте Пароль * ", font=MyText)
        password_lable.place(relx=0.2, rely=0.56, anchor="center")
     
        password_entry = tk.Entry(self, textvariable=self.password, show="*", font=EntryText)
        password_entry.place(relx=0.6, rely=0.56, anchor="center")


        password_lable1 = tk.Label(self, text="Повторите Пароль * ", font=MyText)
        password_lable1.place(relx=0.2, rely=0.62, anchor="center")
     
        password_entry1 = tk.Entry(self, textvariable=self.rpassword, show="*", font=EntryText)
        password_entry1.place(relx=0.6, rely=0.62, anchor="center")


        button_register = tk.Button(self, text="Создать", font=MyText,
                            command=lambda: [self.check_register_data()])
        button_register.place(relx=0.4, rely=0.75, anchor="center")

        button_back = tk.Button(self, text="Назад", font=MyText,
                    command=lambda: controller.show_frame(StartPage))
        
        button_back.place(relx=0.6, rely=0.75, anchor="center")
        

    def check_register_data(self):
        fname = str(self.username.get()).strip()
        password = str(self.password.get()).strip()
        rpassword = str(self.rpassword.get()).strip()


        if rpassword != password:
            messagebox.showwarning(title='ошибка', message="пароли не совпадают")

        if fname.isspace() or password.isspace() or ' ' in fname or ' ' in password or len(fname) == 0 or len(password) == 0:   
            messagebox.showwarning(title='ошибка', message='неверно указаны данные')
            
        else :
            if (self.is_overwrite_data(fname)):
                messagebox.showwarning(title='ошибка', message='логин уже существует')
            else :
                self.add_register_data()
                messagebox.showinfo(title='Успешно!', message="Аккаунт создан успешно")
                self.ctrl.show_frame(StartPage)
            
        
        self.username.set("")
        self.password.set("")
        self.rpassword.set("")
        
    def add_register_data(self):
        data = open("GUI\profiles.txt", "a")
        data.write(self.username.get() + "|" + self.password.get() + "\n")
        data.close()
        
    def is_overwrite_data(self, name):
        data = open("GUI\profiles.txt", "r")
        name = name + '|'
        if name in data.read():
           data.close()
           return True
        else :
            data.close()
        return False 


