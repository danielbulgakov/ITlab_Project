from turtle import shape
import numpy as np

class SensorDataWorker():

    def __init__(self):
        self.main_arr = np.empty(shape=(6,0))
        pass

    def get_array(self):
        return self.main_arr

    def pack_is_ready(self):
        if self.main_arr.shape == (6, 20):
            print("Ywwww")
            return True
        else:
            print("Nooooo")
            return False

    def add_to_np_array(self, ax, ay, az, gx, gy, gz):
        self.main_arr = np.append(self.main_arr, [ax, ay, az, gx, gy, gz], axis=1)
        print(self.main_arr.shape)
        print("Значеняи Умпешно добавлены")

    def clear_np_arr(self):
        self.main_arr = np.empty(shape=(6,0))
        print(self.main_arr)
        print("Массив почищен")
        
        

    def save_to_file(self):
        np.save('Logs/sensors_data', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.empty(shape=(6,20))
        self.main_arr = np.load('Logs/sensors_data.npy', allow_pickle=True ) 
   

class ArraySensorDataWorker():

    def __init__(self):
        self.main_arr = np.empty(shape=[0, 6, 20])
        print(self.main_arr.shape)
        print(self.main_arr)

    def add_pack(self, data):
        self.main_arr = np.append(self.main_arr, [data], axis=0)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print(self.main_arr.shape)
        print("Умпешно добавлено")

    def get_array(self):
        return self.main_arr 
    
    def save_file(self):
        np.save('Logs/active', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.load('Logs/sensors_data.npy')
        print(self.main_arr.shape)
  
