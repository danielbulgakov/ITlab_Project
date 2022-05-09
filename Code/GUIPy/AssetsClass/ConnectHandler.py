from re import T
import threading
import struct as strct
import serial
import random
import numpy as np

from AssetsClass.SensorsData import ArraySensorDataWorker, SensorDataWorker
import AssetsClass.GlobalVariables as gb

class ConnectHandler():

    def __init__(self):
        self.main_arr = ArraySensorDataWorker()
        self.ActiveState = False
        self.threadisrun = False
        self.ax = [] 
        self.ay = [] 
        self.az = []
        self.gx = [] 
        self.gy = [] 
        self.gz = []
        self.pulse = [] 
        self.sp02 = [] 
        self.time = [] 
        pass
    
     

    def connect(self, port, baudrate, serialData):
        self.ActiveState = True
        self.port = port
        self.baud = baudrate
        self.serialData = serialData
        self.ser = serial.Serial(self.port, self.baud)

        
    
    def createthread(self):
        self.ActiveState = True
        t1 = threading.Thread(target= self.readSerial)
        t1.daemon = True
        t1.start()


    def readSerial(self):
        global sd
        self.ActiveState = True
        print("thread start")
        #self.serialData
        if not self.serialData:
            self.data_destroy()
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

                    check6 = strct.unpack('10c', data6)
                    # print(check6)
                    # print("##########################")
                    
                    
                    if (check1 != (b'<', b'S', b't', b'a', b'r', b't', b'_', b'P', b'a', b'c', b'k') or
                    check6 != (b'E', b'n', b'd', b'_', b'P', b'a', b'c', b'k', b'>', b'\x00')) :
                        continue
                    
                    #показания гиро и акса
                    check2 = strct.unpack('60f', data2)
                    # print(check2)
                    #pulse
                    check3 = strct.unpack('10B', data3)
                    # print(check3)
                    #spo2
                    check4 = strct.unpack('10f', data4)
                    # print(check4)
                    #время
                    check5 = strct.unpack('7B', data5)
                    # print(check5)

                    #мы можем их не удалять и посмотреть что получится)
                    self.data_destroy()
                    #заполнение массивов
                    for i in range(0, 10):
                        self.ax.append(check2[i])

                    for i in range(10, 20):
                        self.ay.append(check2[i])

                    for i in range(20, 30):
                        self.az.append(check2[i])

                    for i in range(30, 40):
                        self.gx.append(check2[i])
                    
                    for i in range(40, 50):
                        self.gy.append(check2[i])

                    for i in range(50, 60):
                        self.gz.append(check2[i])

                    for i in range(0, 10):
                        self.pulse.append(check3[i])

                    for i in range(0, 10):
                        self.sp02.append(check4[i])

                    for i in range(0, 7):
                        if i == 2:
                            self.time.append(check5[i] * 100 + check5[i + 1])
                            i += 1
                            continue
                        if i == 3: continue
                        self.time.append(check5[i])
                    
                    if gb.sd.pack_is_ready() is False:
                        gb.sd.add_to_np_array(self.ax, self.ay, self.az, self.gx, self.gy, self.gz)
                    else:
                        self.main_arr.add_pack(gb.sd.get_array())
                        gb.sd.clear_np_arr()

                            
                    
                    

                    print("АксX:")
                    print(self.ax)
                    print("АксY:")
                    print(self.ay)
                    print("АксZ:")
                    print(self.az)
                    print("ГироX:")
                    print(self.gx)
                    print("ГироY:")
                    print(self.gy)
                    print("ГироZ:")
                    print(self.gz)
                    print("Пульс:")
                    print(self.pulse)
                    print("Кислород:")
                    print(self.sp02)
                    print("Время:")    
                    print(self.time)


                except:
                    pass

    def GetSpO2(self):
        temp = self.sp02.copy()
        self.sp02.clear()
        # temp = list(float(random.choice(range(92, 100))) for _ in range(10))
        # print(temp)
        return temp

    def GetPulse(self):
        temp = self.pulse.copy()
        self.pulse.clear()
        # temp = list(float(random.choice(range(80, 110))) for _ in range(10))
        # print(temp)
        return temp
    
    def GetAx(self):
        return self.ax
    
    def GetAy(self):
        return self.ay
    
    def GetAz(self):
        return self.az

    def GetGx(self):
        return self.gx
    
    def GetGy(self):
        return self.gy
    
    def GetGz(self):
        return self.gz 

    def GetTime(self):
        return self.time 


    def data_destroy(self):
        self.ax*= 0
        self.ay*= 0
        self.az*= 0
        self.gx*= 0
        self.gy*= 0
        self.gz*= 0
        self.pulse*= 0
        self.sp02*= 0
        self.time*= 0


    def enddata(self, serialData):
        self.main_arr.save_file()
        self.data_destroy()
        self.serialData = serialData

    def getconditionthread(self):
        return self.threadisrun

    def setconditionthread(self, threadcondition):
        self.data_destroy()
        self.threadisrun = threadcondition
    