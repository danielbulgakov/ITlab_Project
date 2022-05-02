#include <Arduino.h>
#include "MPU6050.h"
#include "I2Cdev.h"
#include <BluetoothSerial.h>
#include <iostream>
#include <ctime>

void CreateData();
void TranslatePack();

byte packet[318];
const int size = 318;
float wx[10],wy[10],wz[10]; // Угловое ускорение
float  x[10], y[10], z[10]; // Гирскоп
byte Pulse[10]; float SpO2[10]; // Пульс, Оксиденация
byte Time[7]; // Время [день, месяц, год / 10, год % 100, часы, минуты, секунды]

MPU6050 mpu;

int16_t ax, ay, az;
int16_t gx, gy, gz;

float ax_f, ay_f, az_f;
float gx_f, gy_f, gz_f;

int count = 0;

BluetoothSerial MY_ESP32;  

void setup() {
  srand(time(NULL));

  for (int i = 0; i < 10; i++)
  {
    Pulse[i] = rand() % 20 + 70;
    SpO2[i] = rand() % 10 + 90;
  }

  Time[0] = 2; Time[1] = 5; Time[2] = 20; Time[3] = 22; Time[4] = 15; Time[5] = 33; Time[6] = 20;

  Serial.begin(115200);
  Wire.begin();
  MY_ESP32.begin("ESP32-K");
  mpu.initialize();
  Serial.print("Nice day");
  delay(1000);
}

void loop() {
  byte arr[10];

  const char endmess[10] = "End_Pack>";

  for (int i = 0; i < 10; i++)
  {
    arr[i] = endmess[i];
  }
  

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  //MY_ESP32.print(str);
  ax_f = (2 * 9.82 * ax) / 32768;
  ay_f = (2 * 9.82 * ay) / 32768;
  az_f = (2 * 9.82 * az) / 32768;
  
  gx_f = (250 * gx) / 32768;
  gy_f = (250 * gy) / 32768;
  gz_f = (250 * gz) / 32768;
  
  /*
  memcpy(arr, &(ax_f), sizeof(float));
  memcpy(arr + 4, &(ay_f), sizeof(float));
  memcpy(arr + 8, &(az_f), sizeof(float));
  memcpy(arr + 12, &(gx_f), sizeof(float));
  memcpy(arr + 16, &(gy_f), sizeof(float));
  memcpy(arr + 20, &(gz_f), sizeof(float));
  */

  wx[count] = ax_f; wy[count] = ay_f; wz[count] = az_f; x[count] = gx_f; y[count] = gy_f; z[count] = gz_f;

  /*
  Serial.print("Accelerometer ");
  Serial.print("X: ");
  Serial.print((double)ax_f);
  Serial.print(" m/s^2, ");
  Serial.print("Y: ");
  Serial.print((double)ay_f);
  Serial.print(" m/s^2, ");
  Serial.print("Z: ");
  Serial.print((double)az_f);
  Serial.println(" m/s^2");

  Serial.print("Gyroscope ");
  Serial.print("X: ");
  Serial.print((double)gx_f);
  Serial.print(" rps, ");
  Serial.print("Y: ");
  Serial.print((double)gy_f);
  Serial.print(" rps, ");
  Serial.print("Z: ");
  Serial.print((double)gz_f);
  Serial.println(" rps");
  */
  count++;
  if(count == 10)
  {
    CreateData();
    MY_ESP32.write(packet, 318);
    TranslatePack();
    count = 0;
    delay(200);
  }
  //MY_ESP32.write(arr, 10);
  
  delay(50);
}

void CreateData()
{
  for (int i = 0; i < 10; i++)
  {
    Pulse[i] = rand() % 20 + 70;
    SpO2[i] = rand() % 10 + 90;
  }

  const char startmess[12] = "<Start_Pack";
  const char endmess[10] = "End_Pack>";

  for(int i = 0; i < 11; i++) //было 12
  {
    packet[i] = startmess[i];
  }

  int startoffset = 11; //было 12
        

  for(int i = 0; i < 10; i++){
    memcpy(packet + startoffset + i * sizeof(float), &(wx[i]), sizeof(float));
    memcpy(packet + startoffset + i * sizeof(float) + 40, &(wy[i]), sizeof(float));
    memcpy(packet + startoffset + i * sizeof(float) + 40 * 2, &(wz[i]), sizeof(float));
    memcpy(packet + startoffset + i * sizeof(float) + 40 * 3, &(x[i]), sizeof(float));
    memcpy(packet + startoffset + i * sizeof(float) + 40 * 4, &(y[i]), sizeof(float));
    memcpy(packet + startoffset + i * sizeof(float) + 40 * 5, &(z[i]), sizeof(float));
  }
  startoffset += 240;
        
  for (int i = 0; i < 10; i++)
  {
    packet[i + startoffset ] = Pulse[i];
  }    
        
  startoffset += 10;

  for (int i = 0; i < 10; i++)
  {
    memcpy(packet + startoffset + i * sizeof(float), &(SpO2[i]), sizeof(float));
  }

  startoffset += 40;

  for (int i = 0; i < 7; i++)
  {
    packet[startoffset + i] = Time[i];
  }

  startoffset += 7;

   for(int i = 0; i < 9; i++) //было 10
  {
    packet[startoffset + i] = endmess[i];//вместо 9 было 10
  }
        
}

void TranslatePack()
{
        char startmess[12];
        char endmess[10];
        float wx[10],wy[10],wz[10];
        float  x[10], y[10], z[10];
        byte Pulse[10]; float SpO2[10];
        byte Time[7];

        int PulseInt[10], TimeInt[6];

        for (int i = 0; i < 11; i++)
            startmess[i] = packet[i];
        startmess[11] = '\0';

        
        for (int i = 0; i < 10; i++)
        {
            float test;
            memcpy(&test, packet + 11 + i * sizeof(float), sizeof(uint8_t) * 4);
            wx[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 40, sizeof(uint8_t) * 4);
            wy[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 80, sizeof(uint8_t) * 4);
            wz[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 120, sizeof(uint8_t) * 4);
            x[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 160, sizeof(uint8_t) * 4);
            y[i] = test;

            memcpy(&test, packet + 11 + i * sizeof(float) + 200, sizeof(uint8_t) * 4);
            z[i] = test;   
        }

        for (int i = 0; i < 10; i++)
        {
            uint8_t test;
            memcpy(&test, packet + 11 + 240 + i * sizeof(uint8_t), sizeof(uint8_t));
            Pulse[i] = test;
            PulseInt[i] = (int)test;            
        }
        
        for (int i = 0; i < 10; i++)
        {
            float test;
            memcpy(&test, packet + 11 + 240 + 10 + i * sizeof(float), sizeof(uint8_t) * 4);
            SpO2[i] = test;            
        }

        for (int i = 0, k = 0; i < 7; i++, k++)
        {
            uint8_t test;
            if (i == 2)
            {                
                memcpy(&test, packet + 11 + 240 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
                Time[i] = test;
                TimeInt[i] = test * 100;
                i++;
                memcpy(&test, packet + 11 + 240 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
                Time[i] = test;
                TimeInt[k] += test;
                i++;
                k++;
            }
            memcpy(&test, packet + 11 + 240 + 10 + 40 + i * sizeof(uint8_t), sizeof(uint8_t));
            Time[i] = test;
            TimeInt[k] = (int)test;            
        }
        
        for (int i = 0; i < 10; i++)
            endmess[i] = packet[i + 11 + 240 + 10 + 40 + 7];
        endmess[10] = '\0';
        
        //toString все величины
        String sstrm = "Начало пакета: ", sendm = "Конец пакета: ", swx = "Показание акселерометра по оси X: ", swy = "Показание акселерометра по оси Y: " , 
        swz = "Показание акселерометра по оси Z: ", sx = "Показание гироскопа по оси X: ", sy = "Показание гироскопа по оси Y: ", 
        sz = "Показание гироскопа по оси Z: ", spulse = "Показание пульса: ", 
        sspo2 = "Показание кислорода в кроваи: ", stime = "Время начала пакета: ";

        for (int i = 0; i < 11; i++)
            sstrm += String(startmess[i]);
        
        for (int i = 0; i < 10; i++)
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
