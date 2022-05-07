import numpy as np


class ArraySensorDataWorker:

    def __init__(self):
        self.main_arr = np.empty(shape=[0, 6, 20])
        print(self.main_arr.shape)
        print(self.main_arr)

    def add_pack(self, data):
        self.main_arr = np.append(self.main_arr, [data], axis=0)
        print(self.main_arr.shape)
        print("Умпешно добавлено")

    def get_array(self):
        return self.main_arr

    def save_file(self):
        np.save('sensors_data', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.load('sensors_data.npy')
        print(self.main_arr.shape)
        # print(np.array([self.main_arr, self.main_arr]).shape)


d = ArraySensorDataWorker()
d.load_sensor_data()
# d.add_pack(s.get_array())
# d.add_pack(s.get_array())
print(d.get_array())
