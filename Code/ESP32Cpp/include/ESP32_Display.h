#ifndef _ESP32_Display_
#define _ESP32_Display_

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//
//  Connect SSD1306 (128x64) display to ESP32
//


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels


class ESP32_Display {
private:

    Adafruit_SSD1306 display; 

public:

    ESP32_Display(){
        display = Adafruit_SSD1306(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
    }


    // Begin SSD1306 wire 

    void _init_(){ 
        if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
            Serial.println(F("SSD1306 allocation failed"));
            for(;;);
        }
    }

    // Print static text on display

    void PrintText(String text){  
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(WHITE);
        display.setCursor(0, 10);
        display.println(text);
        display.display(); 
    }

    // Print static text on display
    
    void PrintText(String text, int color, int size, int posX, int posY){
        display.clearDisplay();
        display.setTextSize(size);
        display.setTextColor(color);
        display.setCursor(posX, posY);
        display.println(text);
        display.display(); 
    }
};


#endif
