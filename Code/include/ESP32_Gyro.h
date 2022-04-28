#ifndef _ESP32_Gyro_
#define _ESP32_Gyro_

#include <Adafruit_MPU6050.h>

//
//  Connect MPU6050 Gyro, Accel and Temp sensor to ESP32
//

#define MPU6050_AO_HIGH 0x69
#define MPU6050_AO_LOW  0x68
#define MPU6050_A0_DEFAULT MPU6050_AO_LOW


class ESP32_Gyro {
private:

    Adafruit_MPU6050 mpu;
    sensors_event_t a, g, temp;
    int MPU_ADDR = MPU6050_AO_HIGH;

public:

    // Begin MPU6050 wire

    void _init_(int i2c_addr = MPU6050_A0_DEFAULT){

        MPU_ADDR = i2c_addr;

          if (!mpu.begin(MPU_ADDR)) {
            Serial.println("Sensor init failed");
            for(;;);
        }
        
    }

    // Print All Data in SerialPort
    float Getwx(){
        mpu.getEvent(&a, &g, &temp);
        return a.acceleration.x;
    }

    float Getwy(){
        mpu.getEvent(&a, &g, &temp);
        return a.acceleration.y;
    }

    float Getwz(){
        mpu.getEvent(&a, &g, &temp);
        return a.acceleration.z;
    }

    float Getx(){
        mpu.getEvent(&a, &g, &temp);
        return g.gyro.x;
    }

    float Gety(){
        mpu.getEvent(&a, &g, &temp);
        return g.gyro.y;
    }

    float Getz(){
        mpu.getEvent(&a, &g, &temp);
        return g.gyro.z;
    }

    void SerialPrint(){
        mpu.getEvent(&a, &g, &temp);
        Serial.print("Accelerometer ");
        Serial.print("X: ");
        Serial.print(a.acceleration.x, 1);
        Serial.print(" m/s^2, ");
        Serial.print("Y: ");
        Serial.print(a.acceleration.y, 1);
        Serial.print(" m/s^2, ");
        Serial.print("Z: ");
        Serial.print(a.acceleration.z, 1);
        Serial.println(" m/s^2");

        Serial.print("Gyroscope ");
        Serial.print("X: ");
        Serial.print(g.gyro.x, 1);
        Serial.print(" rps, ");
        Serial.print("Y: ");
        Serial.print(g.gyro.y, 1);
        Serial.print(" rps, ");
        Serial.print("Z: ");
        Serial.print(g.gyro.z, 1);
        Serial.println(" rps");

    }

    // Return String of Acceleration Data 

    String AccelData(){ 
        mpu.getEvent(&a, &g, &temp);
        String Data;
        Data += "Accelerometer - m/s^2 " + String(a.acceleration.x) + ", " + String(a.acceleration.y )
                + ", " + String(a.acceleration.z);
        return(Data);
    }   

    // Return String of Gyroscope Data 
    
    String GyroData(){
        mpu.getEvent(&a, &g, &temp);
        String Data;
        Data += "Gyroscope X: " + String(g.gyro.x) + " rps, " + "Y: " + String(g.gyro.y) + " rps, "+
                "Z: " + String(g.gyro.z) + " rps, ";
        return(Data);

    }

};
#endif