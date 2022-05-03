#include <ESP32_Display.h>
#include <ESP32_Time.h>
#include <ESP32_NTP.h>
#include <ESP32_Gyro.h>
#include <ESP32_Check.h>
#include <ESP32_SDcard.h>




// SDA - 21 // SCL - 22 //

#include <Adafruit_Sensor.h>
#include <Wire.h>



//ESP32_Display ESP32_display;
ESP32_Gyro ESP32_gyro;
ESP32_Time ESP32_time;
//ESP32_SDcard ESP32_sdcard;






void setup () {
  
  Serial.begin(115200);
  ESP32_sdcard._init_();

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

        ESP32_sdcard.listDir(  "/", 0);
        ESP32_sdcard.createDir(  "/mydir");
        ESP32_sdcard.listDir(  "/", 0);

        ESP32_sdcard.listDir(  "/", 2);
        ESP32_sdcard.writeFile(  "/hello.txt", "Hello ");
        ESP32_sdcard.appendFile(  "/hello.txt", "World!\n");
        ESP32_sdcard.readFile(  "/hello.txt");


        Serial.printf("Total space: %lluMB\n", SD.totalBytes() / (1024 * 1024));
        Serial.printf("Used space: %lluMB\n", SD.usedBytes() / (1024 * 1024));

  
  delay(4000);



}
