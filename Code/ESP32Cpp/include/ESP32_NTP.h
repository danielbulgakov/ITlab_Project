#ifndef _ESP32_NTP_
#define _ESP32_NTP_

#include <WiFi.h>
#include "time.h"

const char* ssid       = "TP-Link_C76A";
const char* password   = "75484927";

const char* ntpServer = "europe.pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;

void printLocalTime()
{
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    struct tm timeinfo;
    if(!getLocalTime(&timeinfo)){
        Serial.println("Failed to obtain time");
        return;
     }
    Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
}

time_t GetLocalTime(){
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    struct tm timeinfo;

    /* get current timeinfo and modify it to the user's choice */

    if(!getLocalTime(&timeinfo)){
        Serial.println("Failed to obtain time");
        return mktime(0L);
    }
    timeinfo.tm_hour+=3;
    time_t timeSinceEpoch = mktime(&timeinfo);
    time(&timeSinceEpoch); 

   Serial.println(ctime(&timeSinceEpoch));
    return mktime(&timeinfo);

}

void WiFi_OFF(){
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
}

void WiFi_ON(){
    Serial.printf("Connecting to %s ", ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println(" CONNECTED");
}

#endif