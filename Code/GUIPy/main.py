from email import message
import tkinter as tk
from tkinter import messagebox

from setuptools import Command


LARGE_FONT= ("Verdana", 12)
BOLD= 'Arial 17 bold'
NORMAL= 'Arial 15 bold'


class FramesHandler(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        width = 900 
        height = 900

        self.geometry(str(width) + "x" + str(height))
        self.minsize(900, 900)
        self.title("ESPушка")
        
        self.frames = {}

        for F in (StartPage, SignInPage, SignUpPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Выберите способ авторизации", font=BOLD)
        label.place(relx=0.5, rely=0.4, anchor="center")
            
        login_button = tk.Button(self, text="Войти", height="2", width="30",font=NORMAL, command=lambda: controller.show_frame(SignInPage))
        login_button.place(relx=0.5, rely=0.5, anchor="center" )
            
        signin_button = tk.Button(self ,text="Зарегистрироваться", height="2", width="30",font=NORMAL , command=lambda: controller.show_frame(SignUpPage))
        signin_button.place(relx=0.5, rely=0.6, anchor="center")


class SignInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.ctrl = controller
                
        label = tk.Label(self, text="Войдите в аккаунт", font=BOLD)
        label.place(relx=0.5, rely=0.4, anchor="center")
        
        
        username_lable = tk.Label(self, text="Логин * ", font=NORMAL)
        username_lable.place(relx=0.4, rely=0.5, anchor="center")
     
        
        username_entry = tk.Entry(self, textvariable=self.username, font=NORMAL)
        username_entry.place(relx=0.6, rely=0.5, anchor="center")
        
        password_lable = tk.Label(self, text="Пароль * ", font=NORMAL)
        password_lable.place(relx=0.4, rely=0.56, anchor="center")
     
        
        password_entry = tk.Entry(self, textvariable=self.password, font=NORMAL)
        password_entry.place(relx=0.6, rely=0.56, anchor="center")

        button_register = tk.Button(self, text="Вход", font=NORMAL,
                            command=lambda: [self.check_register_data()])
        button_register.place(relx=0.4, rely=0.65, anchor="center")

        button_back = tk.Button(self, text="Назад", font=NORMAL,
                    command=lambda: controller.show_frame(StartPage))
        
        button_back.place(relx=0.6, rely=0.65, anchor="center")
        
    def check_register_data(self):
        fname = str(self.username.get()).strip()
        password = str(self.password.get()).strip()
        

            
        if fname.isspace() or password.isspace() or ' ' in fname or ' ' in password or len(fname) == 0 or len(password) == 0:   
            messagebox.showwarning(title='ошибка', message='неверно указаны данные')
            
        else :
            if self.find_register_data() :
                self.ctrl.show_frame(StartPage)
            else : 
                messagebox.showwarning(title='ошибка', message='неверно логин или пароль')
            
        
        self.username.set("")
        self.password.set("")
        
    def find_register_data(self):
        data = open("data.txt", "r")
        if (self.username.get() + "|" + self.password.get() + "\n") in data : 
            data.close()
            return True;
        data.close()
        return False;


class SignUpPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.ctrl = controller
                
        label = tk.Label(self, text="Создание аккаунта", font=BOLD)
        label.place(relx=0.5, rely=0.4, anchor="center")
        
        
        username_lable = tk.Label(self, text="Логин * ", font=NORMAL)
        username_lable.place(relx=0.4, rely=0.5, anchor="center")
     
        
        username_entry = tk.Entry(self, textvariable=self.username, font=NORMAL)
        username_entry.place(relx=0.6, rely=0.5, anchor="center")
        
        password_lable = tk.Label(self, text="Пароль * ", font=NORMAL)
        password_lable.place(relx=0.4, rely=0.56, anchor="center")
     
        
        password_entry = tk.Entry(self, textvariable=self.password, font=NORMAL)
        password_entry.place(relx=0.6, rely=0.56, anchor="center")

        button_register = tk.Button(self, text="Регистрация", font=NORMAL,
                            command=lambda: [self.check_register_data()])
        button_register.place(relx=0.4, rely=0.65, anchor="center")

        button_back = tk.Button(self, text="Назад", font=NORMAL,
                    command=lambda: controller.show_frame(StartPage))
        
        button_back.place(relx=0.6, rely=0.65, anchor="center")
        
        

        
    def check_register_data(self):
        fname = str(self.username.get()).strip()
        password = str(self.password.get()).strip()
        
        

            
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
        
    def add_register_data(self):
        data = open("data.txt", "a")
        data.write(self.username.get() + "|" + self.password.get() + "\n")
        data.close()
        
    def is_overwrite_data(self, name):
        data = open("data.txt", "r")
        name = name + '|'
        if name in data.read():
           data.close()
           return True
        else :
            data.close()
        return False 
        
        
        
        
            
    


        
        
        
        
        

def main_app_screen() :
    app = FramesHandler()
    app.mainloop()
    

main_app_screen()