#ifndef _ESP32_MAX30102_
#define _ESP32_MAX30102_

#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

class ESP32_MAX30102{
private:

    MAX30105 particleSensor;
    const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
    byte* rates; //Array of heart rates
    byte rateSpot = 0;
    long lastBeat = 0; //Time at which the last beat occurred
    float beatsPerMinute;
    int beatAvg;

    long irValue;
    long delta;

public:
    ESP32_MAX30102(){
        return;
    }
    void _init_(){
        rates = new byte[RATE_SIZE];

        // Initialize sensor
        if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
        {
        Serial.println("MAX30105 was not found. Please check wiring/power. ");
        while (1);
        }
        Serial.println("Place your index finger on the sensor with steady pressure.");

        particleSensor.setup(); //Configure sensor with default settings
        particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
        particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED

    }

    void GetDataFromMAX30102(){
        irValue = particleSensor.getIR(); 
        //Serial.print("IR Value  "); Serial.print(irValue);  
        //Serial.println("   Get data function");            //  Считываем значение отражённого ИК-светодиода (отвечающего за пульс) и
        if (checkForBeat(irValue) == true) {
            //Serial.println("Start if");
            //Serial.print(beatAvg);
            //Serial.println("Data fun");                  //  если пульс был зафиксирован, то
            delta = millis() - lastBeat;                   //  находим дельту по времени между ударами
            lastBeat = millis();                                //  Обновляем счётчик
            beatsPerMinute = 60 / (delta / 1000.0);             //  Вычисляем количество ударов в минуту
            if (beatsPerMinute < 255 && beatsPerMinute > 20) {  //  Если количество ударов в минуту находится в промежутке между 20 и 255, то
            rates[rateSpot++] = (byte)beatsPerMinute;         //  записываем это значение в массив значений ЧСС
            rateSpot %= RATE_SIZE;                            //  Задаём порядковый номер значения в массиве, возвращая остаток от деления и присваивая его переменной rateSpot
            beatAvg = 0;                                      //  Обнуляем переменную и
            for (byte x = 0 ; x < RATE_SIZE ; x++) {          //  в цикле выполняем усреднение значений (чем больше RATE_SIZE, тем сильнее усреднение)
                beatAvg += rates[x];                            //  путём сложения всех элементов массива
            }
            beatAvg /= RATE_SIZE;                             //  а затем деления всей суммы на коэффициент усреднения (на общее количество элементов в массиве)
            }
        }
    }

    String GetIR(){
        // GetDataFromMAX30102();
        return String(irValue);
    }

    String GetBPM(){
        // GetDataFromMAX30102();
        return String(beatsPerMinute);
    }

    String GetAvgBPM(){
        return String(beatAvg);
    }

    byte bGetIR(){
        // GetDataFromMAX30102();
        return byte(irValue);
    }

    byte bGetBPM(){
        // GetDataFromMAX30102();
        return byte(beatsPerMinute);
    }

    byte bGetAvgBPM(){
        return byte(beatAvg);
    }

};

#endif  