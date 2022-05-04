#класс для работы с данными пользователя

class WorkerUsersData():

    def __init__(self):
        pass        

    def find_data(self):
        file = open("Logs\data_of_users.txt", "r")
        i = 1
        for line in file:
            data = line
            list_of_lines = data.split("|")
            if list_of_lines[0] == self.user_login:
                file.close()
                return i
            i += 1
        file.close()    
        return 0

    def set_user_login(self, login):
        self.user_login = login[0]

    def printlogin(self):
        #print("А вот и логин")
        #print(self.user_login)
        #print("Логин выше")
        pass

    def write_data_in_file(self, name, surname, phone, email, weight, height, age):
        data = open("Logs\data_of_users.txt", "a")
        data.write(self.user_login + "|" + name + "|" + surname + "|" + phone + "|" + email + "|" + weight + "|" + height + "|" + age + "|" + "\n")
        data.close()
    
    def rewrite_data_in_file(self, name, surname, phone, email, weight, height, age, index):
        file = open("Logs\data_of_users.txt","r")
        lines = file.readlines()
        file.close()
        file = open("Logs\data_of_users.txt","w")
        i = 1
        for line in lines:
            if i == index:
                file.write(self.user_login + "|" + name + "|" + surname + "|" + phone + "|" + email + "|" + weight + "|" + height + "|" + age + "|" + "\n")
            else:
                file.write(line)
            i += 1
        file.close()

    def get_download_data(self):
        arr = []
        file = open("Logs\data_of_users.txt", "r")
        for line in file:
            data = line
            list_of_lines = data.split("|")
            if list_of_lines[0] == self.user_login:
                for word in list_of_lines:
                    arr.append(word)
                break
        file.close()
        #print(arr) # для отладки
        return arr    
