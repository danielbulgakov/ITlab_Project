from turtle import shape
import numpy as np

class SensorDataWorker():

    def __init__(self):
        self.main_arr = np.empty(shape=(6,180))
        pass

    # def create_np_array(self, ax, ay, az, gx, gy, gz):
    #     self.main_arr = np.array([ax, ay, az, gx, gy, gz])
    #     print(self.main_arr)
    def get_array(self):
        return self.main_arr

    #давайте выкинем time, он не подходит для нашего numpy
    def add_to_np_array(self, ax, ay, az, gx, gy, gz):
        self.main_arr = np.append(self.main_arr, [ax, ay, az, gx, gy, gz], axis=1)
    
    def add_to_np_array(self, ax):
        self.main_arr = np.append(self.main_arr, ax, axis=1)
        

    def save_to_file(self):
        np.save('Logs/sensors_data', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.empty(shape=(6,180))
        self.main_arr = np.load('Logs/sensors_data.npy', allow_pickle=True ) 
        # print(np.array([self.main_arr, self.main_arr]).shape)

class ArraySensorDataWorker():

    def __init__(self):
        self.main_arr = np.empty(shape=[0, 6, 180])
        # print(self.main_arr.shape)

    def add_pack(self, data):
        self.main_arr = np.append(self.main_arr, [data], axis=0)
        print(self.main_arr.shape)

    def get_array(self):
        return self.main_arr 
    
    def save_file(self):
        np.save('Logs/sensors_data', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.load('Logs/sensors_data.npy') 
        # print(np.array([self.main_arr, self.main_arr]).shape)

# s = SensorDataWorker()
# s.load_sensor_data()
# # s.add_to_np_array(s.get_array())
# print(s.get_array().shape)
d = ArraySensorDataWorker()
d.load_sensor_data()
print(d.get_array())
# d.add_pack(s.get_array())
# d.add_pack(s.get_array())
# d.save_file()
# d.add_to_np_array(s,s,s,s,s,s)
# s1 = ArraySensorDataWorker()
# s1.add_pack(s)
# s1.add_pack(s)
# s1.save_file()
# s1.load_sensor_data()

# x1 = [1,2,3]
# x2 = [1,2,3]
# x3 = [1,2,3]
# x4 = [1,2,3]
# x5 = [1,2,3]
# x6 = [1,2,3]

# z1 = [1,5,3]
# z2 = [1,5,3]
# z3 = [1,5,3]
# z4 = [1,5,3]
# z5 = [1,5,3]
# z6 = [1,5,3]


# s = np.array([[x1,x2,x3,x4,x5,x6]])
# print(s)

# s1 = np.array([z1,z2,z3,z4,z5,z6])
# print(s1)

# s = np.append(s, [s1], axis=0)
# print(s)
