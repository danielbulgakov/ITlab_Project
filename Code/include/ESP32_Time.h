#ifndef _ESP32_Time_
#define _ESP32_Time_

#include "RTClib.h"
#include <ESP32_NTP.h>
#include <TimeLib.h>
#include <time.h>

//
//  Connect DS3231 Real Time Clock to ESP32
//


class ESP32_Time  {
private:
    RTC_DS3231 rtc;

public: 

    // Begin DS3231 wire

    void _init_(){

        if (! rtc.begin()) {
            Serial.println("Couldn't find RTC");
            while (1);
        }

        if (rtc.lostPower()) {
            Serial.println("RTC lost power, lets set the time!");
        }

    }

    // Return String of Time type of 
    // Thu, 16 Apr 2020 18:34:56

    String GetCurrentDateString(){
        String sbuff = "DDD, DD MMM YYYY hh:mm:ss";
        const char* cbuff =  sbuff.c_str();

        DateTime now = rtc.now();
        String Time = String(now.toString((char*)cbuff));      
        return Time;

    }

    // Return String of Time type of 
    // Thu, 16 Apr 2020 18:34:56

    String GetCurrentTimeString(){
        String sbuff = "hh:mm:ss";
        const char* cbuff =  sbuff.c_str();

        DateTime now = rtc.now();
        String Time = String(now.toString((char*)cbuff));      
        return Time;

    }

    int GetDay(){
        DateTime now = rtc.now();
        return now.day();
    }

    int GetMonth(){
        DateTime now = rtc.now();
        return now.month();
    }

    int GetYear(){
        DateTime now = rtc.now();
        return now.year();
    }

    int GetHour(){
        DateTime now = rtc.now();
        return now.hour();
    }

    int GetMin(){
        DateTime now = rtc.now();
        return now.minute();
    }

    int GetSec(){
        DateTime now = rtc.now();
        return now.second();
    }

    // Return String of Time type of 
    // | specifier | output                                                 |
    // |-----------|--------------------------------------------------------|
    // | YYYY      | the year as a 4-digit number (2000--2099)              |
    // | YY        | the year as a 2-digit number (00--99)                  |
    // | MM        | the month as a 2-digit number (01--12)                 |
    // | MMM       | the abbreviated English month name ("Jan"--"Dec")      |
    // | DD        | the day as a 2-digit number (01--31)                   |
    // | DDD       | the abbreviated English day of the week ("Mon"--"Sun") |
    // | AP        | either "AM" or "PM"                                    |
    // | ap        | either "am" or "pm"                                    |
    // | hh        | the hour as a 2-digit number (00--23 or 01--12)        |
    // | mm        | the minute as a 2-digit number (00--59)                |
    // | ss        | the second as a 2-digit number (00--59)                |

    String GetCurentCustomString(String type){

        const char* Type =  type.c_str();

        DateTime now = rtc.now();
        String Time = String(now.toString((char*)Type));      
        return Time;

    }

    // Sync RTC time using NTP protocol 
    // ESP32_NTP.h
    
    void SyncTime(){
        WiFi_ON();
        time_t t = GetLocalTime();
        DateTime set = DateTime(t);
        WiFi_OFF();

        String sbuff = "DDD, DD MMM YYYY hh:mm:ss";
        const char* cbuff =  sbuff.c_str();

        String Set = String(set.toString((char*)cbuff));
        //Serial.println("Set " + Set);
        
        rtc.adjust(set);

        DateTime now = rtc.now();
        String Now = String(now.toString((char*)cbuff));
    }


};


#endif


    

    


 


