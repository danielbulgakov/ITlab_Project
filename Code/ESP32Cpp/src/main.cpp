#include <ESP32_Gyro.h>
#include <ESP32_Time.h>
#include <ESP32_SDcard.h>
#include <ESP32_MAX30102.h>
#include <BluetoothSerial.h>
#include <ESP32_PackageController.h>

// SDA - 21 // SCL - 22 //

#include <Adafruit_Sensor.h>
#include <Wire.h>

volatile byte state = LOW;
hw_timer_t * timer = NULL;

uint32_t MyTimer1 = 0, MyTimer2 = 0;

BluetoothSerial MY_ESP32;

int TimeStamp = 0;

Package pack;
PackageController pcontr; 


ESP32_Gyro ESP32_gyro;
ESP32_Time ESP32_time;
ESP32_SDcard ESP32_sdcard;
ESP32_MAX30102 ESP32_max;

byte counter = 0;



void setup () {

  Serial.begin(115200);
  ESP32_sdcard.Init();
  ESP32_max.Init();
  ESP32_time.Init();
  ESP32_gyro.Init(0x69);
  MY_ESP32.begin("ESP32-K");

  ESP32_max.GetDataFromMAX30102();
 
  

}

void loop () {
  Serial.println(ESP32_time.GetCurrentDateString());
  ESP32_max.UpdateArray();

  if (millis() - MyTimer1 >= 200)
  {
    ESP32_max.UpdateData();

    pack.AddGyro(ESP32_gyro.Getwx(), ESP32_gyro.Getwy(), ESP32_gyro.Getwz(), ESP32_gyro.Getx(), ESP32_gyro.Gety(), ESP32_gyro.Getz());
    pack.AddPulse(ESP32_max.bGetBPM());
    pack.AddSpO2(ESP32_max.fGetSpO2());
    pack.AddTime(ESP32_time.GetDay(), ESP32_time.GetMonth(), ESP32_time.GetYear(), ESP32_time.GetHour(), ESP32_time.GetMin(), ESP32_time.GetSec());

    MyTimer1 = millis();
    counter++;
  } 
  
  if (counter == 10 && pack.isFull()){
    pcontr.CreatePack(pack);
    MY_ESP32.write(pcontr.GetPack(), pcontr.GetSize());
    Serial.println("Пакет отправлен");
    pack.Reset();
    counter = 0;    
  }
}
