#ifndef _ESP32_PACKAGE_CONTROLLER_
#define _ESP32_PACKAGE_CONTROLLER_

#include <Arduino.h>
#include <string.h>
class TPackage;
typedef TPackage Package;

class TPackage
{
protected:
    byte GnWIter = 0, PIter = 0, SIter = 0;

    float wx[100],wy[100],wz[100]; // Угловое ускорение
    float  x[100], y[100], z[100]; // Гирскоп
    byte Pulse[10]; float SpO2[10]; // Пульс, Оксиденация
    byte Time[7]; // Время [день, месяц, год / 10, год % 100, часы, минуты, секунды]
public:

    
    
    byte GetTime(int i){
        return Time[i];
    }

    float* GetSpO2(int i){
        return &SpO2[i];
    }

    float* GetWx(int i){
        return &wx[i];
    }

    float* GetWy(int i){
        return &wy[i];
    }
    
    float* GetWz(int i){
        return &wz[i];
    }

    float* GetX(int i){
        return &x[i];
    }

    float* GetY(int i){
        return &y[i];
    }

    float* GetZ(int i){
        return &z[i];
    }

    byte GetPulse(int i){
        return Pulse[i];
    }

    bool isFull() {return GnWIter >= 100 ;}
    bool isEmpty() {return !isFull();}
    void Reset(){
        GnWIter = 0;
        PIter = 0;
        SIter = 0;
        memset(Time, -1, 7);
    }

    bool AddGyro(float _wx, float _wy, float _wz, float _x, float _y, float _z){
        bool result = false;
        if (GnWIter < 100){
            wx[GnWIter] = _wx;
            wy[GnWIter] = _wy;
            wz[GnWIter] = _wz;
            x[GnWIter] = _x;
            y[GnWIter] = _y;
            z[GnWIter] = _z;

            GnWIter++;
            result = true;
        }
        return result;
    }
    bool AddPulse(byte pulse){
        bool result = false;
        if (PIter < 10){
            Pulse[PIter] = pulse;
            PIter++;
            result = true;
        }
        return result;
    }
    bool AddSpO2(float spo2){
        bool result = false;
        if (SIter < 10){
            SpO2[SIter] = spo2;
            SIter++;
            result = true;
        }
        return result;
    }
    bool AddTime(int d, int m, int y, int h, int mi, int s){
        bool result = false;
        Time[0] = d;
        Time[1] = m;
        Time[2] = y / 100;
        Time[3] = y % 100;
        Time[4] = h;
        Time[5] = mi;
        Time[6] = s;
        result = true;
        return result;
    }


};

class PackageController 
{
private:
    byte packet[2477]; // было 2479
    const int size = 2477; //было 2479
    //BluetoothSerial
public:
    PackageController(){}

    //Метод отправки по блютуз
    byte* GetPacket(){
        return packet;
    }
    //нужен ли метод принятия этих данных?

    void CreatePack(Package& pack){
        const char startmess[12] = "<Start_Pack";
        const char endmess[10] = "End_Pack>";

        for(int i = 0; i < 11; i++) //было 12
        {
            packet[i] = startmess[i];
        }

        for(int i = 0; i < 9; i++) //было 10
        {
            packet[size - 1 - i] = endmess[9 - i - 1];//вместо 9 было 10
        }
        int startoffset = 11; //было 12
        byte dummy;

        

        for(int i = 0; i < 100; i++){
            memcpy(packet + startoffset + i * sizeof(float), pack.GetWx(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 400, pack.GetWy(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 400 * 2, pack.GetWz(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 400 * 3, pack.GetX(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 400 * 4, pack.GetY(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 400 * 5, pack.GetZ(i), sizeof(float));
        }
        startoffset += 2400;
        
        for (int i = 0; i < 10; i++)
        {
            packet[i + startoffset ] = pack.GetPulse(i);
        }    
        
        startoffset += 10;

        for (int i = 0; i < 10; i++)
        {
            memcpy(packet + startoffset + i * sizeof(float), pack.GetSpO2(i), sizeof(float));
        }

        startoffset += 40;

        for (int i = 0; i < 7; i++)
        {
            packet[startoffset + i] = pack.GetTime(i);
        }
        
        Serial.write(packet, 2477);
        Serial.println();
    }


    //метод для проверки правильности перевода данных в массив байт
    void TranslatePack(){
        char startmess[12];
        char endmess[10];
        float wx[100],wy[100],wz[100];
        float  x[100], y[100], z[100];
        byte Pulse[10]; float SpO2[10];
        byte Time[7];

        int PulseInt[10], TimeInt[6];

        for (int i = 0; i < 11; i++)
            startmess[i] = packet[i];
        startmess[11] = '\0';

        
        for (int i = 0; i < 100; i++)
        {
            float test;
            memcpy(&test, packet + 11 + i * sizeof(float), sizeof(uint8_t) * 4);
            wx[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 400, sizeof(uint8_t) * 4);
            wy[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 800, sizeof(uint8_t) * 4);
            wz[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 1200, sizeof(uint8_t) * 4);
            x[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 1600, sizeof(uint8_t) * 4);
            y[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 2000, sizeof(uint8_t) * 4);
            z[i] = test;   
        }

        for (int i = 0; i < 10; i++)
        {
            uint8_t test;
            memcpy(&test, packet + 11 + 2400 + i * sizeof(uint8_t), sizeof(uint8_t));
            Pulse[i] = test;
            PulseInt[i] = (int)test;            
        }
        
        for (int i = 0; i < 10; i++)
        {
            float test;
            memcpy(&test, packet + 11 + 2400 + 10 + i * sizeof(float), sizeof(uint8_t) * 4);
            SpO2[i] = test;            
        }

        for (int i = 0, k = 0; i < 7; i++, k++)
        {
            uint8_t test;
            if (i == 2)
            {
                int j;
                memcpy(&j, packet + 11 + 2400 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t) * 2);
                TimeInt[i] = j;
                memcpy(&test, packet + 11 + 2400 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
                Time[i] = test;
                i++;
                memcpy(&test, packet + 11 + 2400 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
                Time[i] = test;
                i++;
                k++;
                continue;
            }
            memcpy(&test, packet + 11 + 2400 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
            Time[i] = test;
            TimeInt[k] = (int)test;            
        }
        
        for (int i = 0; i < 10; i++)
            endmess[i] = packet[i + 11 + 2400 + 10 + 40 + 7];
        endmess[10] = '\0';
        
        //toString все величины
        String sstrm = "Начало пакета: ", sendm = "Конец пакета: ", swx = "Показание акселерометра по оси X: ", swy = "Показание акселерометра по оси Y: " , 
        swz = "Показание акселерометра по оси Z: ", sx = "Показание гироскопа по оси X: ", sy = "Показание гироскопа по оси Y: ", 
        sz = "Показание гироскопа по оси Z: ", spulse = "Показание пульса: ", 
        sspo2 = "Показание кислорода в кроваи: ", stime = "Время начала пакета: ";

        for (int i = 0; i < 11; i++)
            sstrm += String(startmess[i]);
        
        for (int i = 0; i < 100; i++)
        {
            swx += String(wx[i]) + ",";
            swy += String(wy[i]) + ",";
            swz += String(wz[i]) + ",";
            sx += String(x[i]) + ",";
            sy += String(y[i]) + ",";
            sz += String(z[i]) + ",";
        }
        
        for (int i = 0; i < 10; i++)
        {
            spulse += String(PulseInt[i]) + ",";
            sspo2 += String(SpO2[i]) + ",";
            sendm += String(endmess[i]);
        }
        
        for (int i = 0; i < 6; i++)
        {
            stime += String(TimeInt[i]) + ":";
        }
        //начало пакета
        Serial.println(sstrm);
        //аксель
        Serial.println(swx);
        Serial.println(swy);
        Serial.println(swz);
        //гиро
        Serial.println(sx);
        Serial.println(sy);
        Serial.println(sz);
        //пульс
        Serial.println(spulse);
        //кислород
        Serial.println(sspo2);
        //ВРЕМЯ
        Serial.println(stime);
        //конец пакета
        Serial.println(sendm);
    }
};


#endif

