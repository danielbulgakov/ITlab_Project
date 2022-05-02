#ifndef _ESP32_BLUETOOTHCONRTOLLER_
#define _ESP32_BLUETOOTHCONRTOLLER_

#include "BluetoothSerial.h"

class BluetoothController
{
private:
    BluetoothSerial ESP_BT;
public:

    void _init_(){
        ESP_BT.begin("ESP32");
    }

    void CreateTraslation (byte* pack){
        ESP_BT.write(pack, 2477);
    }

};

#endif // _ESP32_BLUETOOTHCONRTOLLER_