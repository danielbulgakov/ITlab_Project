#ifndef _ESP32_BUTTON_
#define _ESP32_BUTTON_


#include <Arduino.h>

class ESP32_Button{
private:

    int Pin;
    int State;

public:

    void _init_(int pin){
        Pin = pin;
        pinMode(pin, INPUT_PULLUP);
    }

    int GetState(){
        return digitalRead(Pin);
    }
};

#endif