#ifndef _ESP32_PACKAGE_CONTROLLER_
#define _ESP32_PACKAGE_CONTROLLER_

#include <Arduino.h>
#include <string.h>


class TPackage;
typedef TPackage Package;
class TPackage
{
protected:
    byte GnWIter = 0, PIter = 0, SIter = 0, TimeIter;

    float wx[10],wy[10],wz[10]; // Угловое ускорение
    float  x[10], y[10], z[10]; // Гирскоп
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

    bool isFull() {return GnWIter >= 10 ;}
 
    void Reset(){
        GnWIter = 0;
        PIter = 0;
        SIter = 0;
        TimeIter = 0;
        memset(Time, -1, 7);
    }

    bool AddGyro(float _wx, float _wy, float _wz, float _x, float _y, float _z){
        bool result = false;
        if (GnWIter < 10){
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
        if (TimeIter < 1) {
            Time[0] = d;
            Time[1] = m;
            Time[2] = y / 100;
            Time[3] = y % 100;
            Time[4] = h;
            Time[5] = mi;
            Time[6] = s;
            TimeIter++;
            result = true;
        }
        return result;
    }


};

class PackageController 
{
private:
    byte packet[318]; 
    const int size = 318; 
public:

    byte* GetPack(){
        return packet;
    }

    int GetSize(){
        return size;
    }

    void CreatePack(Package& pack){
        const char startmess[12] = "<Start_Pack";
        const char endmess[10] = "End_Pack>";

        for(int i = 0; i < 11; i++) 
        {
            packet[i] = startmess[i];
        }
        
        int startoffset = 11; 
            

        for(int i = 0; i < 10; i++){
            memcpy(packet + startoffset + i * sizeof(float), pack.GetWx(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 40,  pack.GetWy(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 40 * 2,  pack.GetWz(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 40 * 3,  pack.GetX(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 40 * 4,  pack.GetY(i), sizeof(float));
            memcpy(packet + startoffset + i * sizeof(float) + 40 * 5,  pack.GetZ(i), sizeof(float));
        }
        startoffset += 240;
            
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

        startoffset += 7;

        for(int i = 0; i < 9; i++) 
        {
            packet[startoffset + i] = endmess[i];
        }
            
        
    }



    
};


#endif

