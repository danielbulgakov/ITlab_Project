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

        if (checkForBeat(irValue) == true)
        {
        //We sensed a beat!
        delta = millis() - lastBeat;
        lastBeat = millis();

        beatsPerMinute = 60 / (delta / 1000.0);

        if (beatsPerMinute < 255 && beatsPerMinute > 20)
        {
        rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
        rateSpot %= RATE_SIZE; //Wrap variable

        //Take average of readings
        beatAvg = 0;
        for (byte x = 0 ; x < RATE_SIZE ; x++)
        beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
        
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

};

#endif  