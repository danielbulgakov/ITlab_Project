//#include <BluetoothHandler/ESP32_PackageController.h>
//#include <BluetoothHandler/ESP32_BluetoothController.h>
#include <ESP32_Display.h>
#include <ESP32_Time.h>
//#include <ESP32_NTP.h>
//#include <ESP32_Gyro.h>
//#include <ESP32_Check.h>
//#include <ESP32_SDcard.h>
//#include <ESP32_MAX30102.h>


#include "BluetoothSerial.h"


// SDA - 21 // SCL - 22 //

#include <Adafruit_Sensor.h>
#include <Wire.h>


int TimeStamp = 0;

ESP32_Display ESP32_display;
//ESP32_Gyro ESP32_gyro;
ESP32_Time ESP32_time;
//ESP32_SDcard ESP32_sdcard;
//ESP32_MAX30102 ESP32_max;

//TPackage pack;
//PackageController pleace;
//BluetoothController bc;
String BPM, IR;


 BluetoothSerial ESP_BT;



void setup () {
  
  Serial.begin(115200);
  // ESP32_sdcard._init_();
  //ESP32_max._init_();
  ESP_BT.begin("ESP32");
  ESP32_display._init_();
  ESP32_time._init_();
  //ESP32_gyro._init_(0x69);
  //bc._init_();
  //ESP_BT.print("aaaaa");
  //ESP32_time.SyncTime();
  //CHECK_I2C_ID();


  








  ESP32_display.PrintText("Time!", WHITE, 3, 5,5);


  ESP32_time.GetCurrentTimeString();
  // Serial.println("after");
  //delay(2000);

  
  

}

void loop () {
  
  /*ESP32_max.GetDataFromMAX30102();
  ESP32_max.GetDataOxygen();
  
  pack.AddGyro(ESP32_gyro.Getwx(), ESP32_gyro.Getwy(), ESP32_gyro.Getwz(), ESP32_gyro.Getx(), ESP32_gyro.Gety(), ESP32_gyro.Getz());
  pack.AddTime(ESP32_time.GetDay(), ESP32_time.GetMonth(), ESP32_time.GetYear(),
      ESP32_time.GetHour(), ESP32_time.GetMin(), ESP32_time.GetSec() );



  if (TimeStamp > 10){

    pack.AddPulse(ESP32_max.bGetAvgBPM());
    pack.AddSpO2(ESP32_max.bGetBPM());

  
  */
  ESP32_display.PrintText(ESP32_time.GetCurrentTimeString());
  /*ESP32_gyro.SerialPrint(); Serial.println("\n");

    // CHECK_I2C_ID();



  //       // ESP32_sdcard.listDir(  "/", 0);
  //       // ESP32_sdcard.createDir(  "/mydir");
  //       // ESP32_sdcard.listDir(  "/", 0);

  //       // ESP32_sdcard.listDir(  "/", 2);
        
  BPM = "BPM = "  + ESP32_max.GetBPM()  + "  " +  ESP32_max.GetAvgBPM() + " ";
  IR = "IR= " + ESP32_max.GetIR() + "\n ";

  //       ESP32_sdcard.appendFile(  "/Beats.txt", BPM.c_str());
  //       ESP32_sdcard.appendFile(  "/Beats.txt", IR.c_str());
        
  Serial.println(BPM); Serial.print(IR); Serial.print(ESP32_max.GetOxy());

  
  TimeStamp = 0;
  }

  if (pack.isFull())
  {
    pleace.CreatePack(pack);
    pleace.TranslatePack();
    // bc.CreateTraslation(pleace.GetPacket());
    pack.Reset();
    // delay(10000);
  }
  
  //delay(50);
  TimeStamp = TimeStamp + 1;
  */

}
