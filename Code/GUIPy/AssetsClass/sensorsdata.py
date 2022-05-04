import numpy as np

class SensorDataWorker():

    def __init__(self):
        pass

    def create_np_array(self, ax, ay, az, gx, gy, gz, pulse, spo2, time):
        self.main_arr = np.array([ax, ay, az, gx, gy, gz, pulse, spo2, time])
        print(self.main_arr)

    #давайте выкинем time, он не подходит для нашего numpy
    def add_to_np_array(self, ax, ay, az, gx, gy, gz, pulse, spo2, time):
        self.main_arr = np.append(self.main_arr, [ax, ay, az, gx, gy, gz, pulse, spo2, time], axis=1)

    def save_to_file(self):
        np.save('Logs/sensors_data', self.main_arr)

    def load_sensor_data(self):
        self.main_arr = np.delete(self.main_arr, [0,1,2,3,4,5,6,7,8], axis=0)
        self.main_arr = np.load('Logs/sensors_data.npy')
        print(self.main_arr)
