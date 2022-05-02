import threading
import struct as strct
import serial
import random
import numpy as np

# Добавить состояние активен не активен для класса, чтобы данные не гернерировались 
# и не считывались без необдиомсти и не засоряли поток. Иначе ввод данных будет затруднителен (логин в систему)

class ConnectHandler():
    def __init__(self) :
        pass
        
    def connect(self, port, baudrate):
        self.port = port
        self.baud = baudrate
        self.ser = serial.Serial(self.port, self.baud, timeout=0)
        t1 = threading.Thread(target= self.readSerial)
        t1.daemon = True
        t1.start()
        
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
                        print(self.ax)

                    for i in range(10, 20):
                        self.ay.append(check2[i])
                        print(self.ay)

                    for i in range(20, 30):
                        self.az.append(check2[i])
                        print(self.az)

                    for i in range(30, 40):
                        self.gx.append(check2[i])
                        print(self.ay)
                    
                    for i in range(40, 50):
                        self.gy.append(check2[i])
                        print(self.gy)

                    for i in range(50, 60):
                        self.gz.append(check2[i])
                        print(self.gz)

                    for i in range(0, 10):
                        self.pulse.append(check3[i])
                        print(self.pulse)

                    for i in range(0, 10):
                        self.sp02.append(check4[i])
                        print(self.sp02)

                    for i in range(0, 7):
                        self.time.append(check5[i])
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
                except:
                    pass
    def GetSpO2(self):
        self.update()
        print(self.spo2)
        return self.spo2
        
    def update(self):
        self.spo2 = np.random.randint(10,20,size=7)