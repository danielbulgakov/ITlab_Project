#include <ESP32_Display.h>
#include <ESP32_Time.h>
#include <ESP32_NTP.h>
#include <ESP32_Gyro.h>
#include <ESP32_Check.h>
#include <ESP32_SDcard.h>
#include <ESP32_MAX30102.h>





// SDA - 21 // SCL - 22 //

#include <Adafruit_Sensor.h>
#include <Wire.h>



ESP32_Display ESP32_display;
ESP32_Gyro ESP32_gyro;
ESP32_Time ESP32_time;
ESP32_SDcard ESP32_sdcard;
ESP32_MAX30102 ESP32_max;

String BPM, IR;






void setup () {
  
  Serial.begin(115200);
  ESP32_sdcard._init_();
  ESP32_max._init_();

  // ESP32_display._init_();
  // ESP32_time._init_();
  // ESP32_gyro._init_(0x69);
  
  // //ESP32_time.SyncTime();


  








  // ESP32_display.PrintText("Time!", WHITE, 3, 5,5);


  // // ESP32_time.GetCurrentTimeString();
  // // Serial.println("after");
  // // delay(2000);


  // // CHECK_I2C_ID();
  

}

void loop () {
        ESP32_max.GetDataFromMAX30102();
        // ESP32_sdcard.listDir(  "/", 0);
        // ESP32_sdcard.createDir(  "/mydir");
        // ESP32_sdcard.listDir(  "/", 0);

        // ESP32_sdcard.listDir(  "/", 2);
        
        BPM = "BPM = " +  ESP32_max.GetAvgBPM() + " ";
        IR = "IR= " + ESP32_max.GetIR() + "\n ";

        // ESP32_sdcard.appendFile(  "/Beats.txt", BPM.c_str());
        // ESP32_sdcard.appendFile(  "/Beats.txt", IR.c_str());
        
      Serial.print(BPM); Serial.print(IR);

  

  
 



}
