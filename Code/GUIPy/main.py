from email import message
import tkinter as tk
from tkinter import PhotoImage, messagebox

from setuptools import Command

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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
        self.minsize(1200, 900)
        self.title("ESPушка")
    
        # canvas = tk.Canvas(width, height)
        # canvas.pack(fill = "both", expand = True)
        # canvas.create_image( 0, 0, image = PhotoImage(file='gg.jpg'), 
        #              anchor = "nw")
        
        self.frames = {}

        for F in (StartPage, SignInPage, SignUpPage, MainScreen):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def set_min_size(self, height, width):
        self.minsize(width,height)

        
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
        
        password_lable = tk.Label(self, text="Пароль * " ,  font=NORMAL)
        password_lable.place(relx=0.4, rely=0.56, anchor="center")
     
        
        password_entry = tk.Entry(self, textvariable=self.password,show="*", font=NORMAL)
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
                self.ctrl.show_frame(MainScreen)
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
     
        
        password_entry = tk.Entry(self, textvariable=self.password, show="*", font=NORMAL)
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
        
        
        
        
            
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        
        data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': [45000,42000,52000,49000,47000]
        }
        df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])


        data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
                'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
                }
        df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])


        data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
                'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
                }  
        df3 = DataFrame(data3,columns=['Interest_Rate','Stock_Index_Price'])
        
        
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

        figure2 = plt.Figure(figsize=(5,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self)
        line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
        ax2.set_title('Year Vs. Unemployment Rate')

        figure3 = plt.Figure(figsize=(5,4), dpi=100)
        ax3 = figure3.add_subplot(111)
        ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
        scatter3 = FigureCanvasTkAgg(figure3, self) 
        scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax3.legend(['Stock_Index_Price']) 
        ax3.set_xlabel('Interest Rate')
        ax3.set_title('Interest Rate Vs. Stock Index Price')

        button_quit = tk.Button(self, text="Выйти", font=NORMAL,
                    command=lambda: controller.show_frame(StartPage))
        
        button_quit.place(relx=0.95, rely=0.95, anchor="center")

        
        
        
        
        

def main_app_screen() :
    app = FramesHandler()
    app.mainloop()
    

main_app_screen()