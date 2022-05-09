#ifndef _ESP32_MAX30102_
#define _ESP32_MAX30102_

#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"  

class ESP32_MAX30102{
private:


    uint32_t irBuffer[50];   //  32-битный массив данных от сенсора со значениями от ИК-светодиода
    uint32_t redBuffer[50];  //  32-битный массив данных от сенсора со значениями от красного светодиода
    //--------------------------------------------------//
    int32_t bufferLength = 50;                           //  длина буфера данных
    int32_t spo2;                                       //  значение SpO2 (насыщенности крови кислородом)
    int8_t  validSPO2;                                  //  флаг валидности значений сенсора по SpO2
    int32_t heartRate;  
    int32_t lasthr = 80;                                //  значение ЧСС
    int8_t  validHeartRate;  

    MAX30105 particleSensor;


public:
    ESP32_MAX30102(){
        return;
    }
    void Init(){
        if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Использовать стандартный I2C порт, 400kHz скорость
        {
        Serial.println("MAX30105 was not found. Please check wiring/power. ");
        while (1);
        }
        Serial.println("Place your index finger on the sensor with steady pressure.");

        particleSensor.setup(60, 4, 2, 400, 411, 4096); //Конфигурация сенсора
        particleSensor.setPulseAmplitudeIR(60);
        particleSensor.setPulseAmplitudeRed(60); 
        particleSensor.setPulseAmplitudeGreen(0); 

    }

    void GetDataFromMAX30102(){
        for (byte i = 0 ; i < bufferLength ; i++) { 
            while (particleSensor.available() == false) {  //  Опрашиваем сенсор на предмет наличия новых значений
                particleSensor.check();
            }
            redBuffer[i] = particleSensor.getRed();          
            irBuffer[i] = particleSensor.getIR();  
            particleSensor.nextSample();
        }
        maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
        Serial.print(F("HR="));                       //  Выводим текст в монитор последовательного порта
        Serial.print(heartRate, DEC);                   //  Выводим значение переменной   heartRate      в монитор последовательного порта
        Serial.print(F(", HRvalid="));                  //  Выводим текст в монитор последовательного порта
        Serial.print(validHeartRate, DEC);              //  Выводим значение переменной   validHeartRate в монитор последовательного порта
        Serial.print(F(", SPO2="));                     //  Выводим текст в монитор последовательного порта
        Serial.print(spo2, DEC);                        //  Выводим значение переменной   spo2           в монитор последовательного порта
        Serial.print(F(", SPO2Valid="));                //  Выводим текст в монитор последовательного порта
        Serial.println(validSPO2, DEC); 
    }

    void UpdateArray(){
        for (byte i = 25; i < 50; i++) {
            redBuffer[i - 25] = redBuffer[i];
            irBuffer[i - 25] = irBuffer[i];
        }
        //  Получаем новые 25 значений прежде чем переходить к вычислению ЧСС
        for (byte i = 25; i < 50; i++) {
            redBuffer[i] =  particleSensor.getRed();        //  Записываем в массив значения сенсора, полученные при работе с КРАСНЫМ светодиодом
            irBuffer[i] =  particleSensor.getIR();          //  Записываем в массив значения сенсора, полученные при работе с ИК      светодиодом
            particleSensor.nextSample();
        } 

    }

    void UpdateData(){
        maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
        
        if (heartRate < 255 && heartRate > 20) {      //  Если количество ударов в минуту находится в промежутке между 20 и 255, то
            lasthr = heartRate;                       //  а затем деления всей суммы на коэффициент усреднения (на общее количество элементов в массиве)
        }
        else {
            heartRate = lasthr;
        }

        Serial.print(F("HR="));                         //  Выводим текст в монитор последовательного порта
        Serial.print(heartRate, DEC);                   //  Выводим значение переменной   heartRate      в монитор последовательного порта
        Serial.print(F(", HRvalid="));                  //  Выводим текст в монитор последовательного порта
        Serial.print(validHeartRate, DEC);              //  Выводим значение переменной   validHeartRate в монитор последовательного порта
        Serial.print(F(", SPO2="));                     //  Выводим текст в монитор последовательного порта
        Serial.print(spo2, DEC);                        //  Выводим значение переменной   spo2           в монитор последовательного порта
        Serial.print(F(", SPO2Valid="));                //  Выводим текст в монитор последовательного порта
        Serial.println(validSPO2, DEC); 
    }

    String GetBPM(){
        return String(heartRate);
    }

    byte bGetBPM(){
        if (validHeartRate == 0) return 0;
        return byte(heartRate);
    }

    float fGetSpO2(){
        if (validSPO2 == 0) return -1;
        if (spo2 < 0)
            spo2 = 0;
        return (float)spo2;
    }

};

#endif  