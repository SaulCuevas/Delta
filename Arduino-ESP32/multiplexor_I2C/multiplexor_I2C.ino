#include <Wire.h>

// Direcciones I2C
const int MT6701_ADDRESS = 0x06;
const int PCA9548A_ADDRESS = 0x70;

// Tiempo de muestreo
unsigned long lastTime = 0; // Tiempo anterior
unsigned long sampleTime = 5; // Tiempo de muestreo en milisegundos

// Configuracion lectura de datos serial
String str = "";        // String recibida por el microcontrolador
bool strComplete = false;  // bandera de identificacion de String

// Variables globales
uint8_t incremento = 0;

void setup() {
  Wire.begin();
  Serial.begin(115200);
}

void loop() {
  if(millis() - lastTime >= sampleTime){
    if (strComplete) {
      // Pref = str.toFloat();
      PCA9548A_cambio_direccion(0, 0);
      PCA9548A_cambio_direccion(incremento, 1);
      incremento++;
      if(incremento == 8) incremento = 0;
      Serial.println(leerMT6701());
      str = "";
      strComplete = false;
    }

    lastTime = millis();
  }
}

// Funcion de evento en el puerto serial
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    str += inChar;
    if (inChar == '\n') {
      strComplete = true;
    }
  }
}

// Funcion para multiplexor I2C
void PCA9548A_cambio_direccion(uint8_t _channel, bool _on_off) {
  byte a_Escribrir = _on_off ? (0x01 << _channel) : 0x00;
  Wire.beginTransmission(PCA9548A_ADDRESS);
  Wire.write(a_Escribrir);
  Wire.endTransmission();
  Serial.println(a_Escribrir);
}

uint8_t I2C_request_single_byte(int _address, int _reg_addr) {
  uint8_t single_byte = 0;

  Wire.beginTransmission(_address);
  Wire.write(_reg_addr);
  Wire.endTransmission();

  Wire.requestFrom(_address, 1);
  if (Wire.available() >= 1) {
    single_byte = Wire.read();
  }
  Wire.endTransmission();

  return single_byte;
}

// Funcion para leer en grados el encoder magnetico
float leerMT6701() {
  byte slaveByte1 = I2C_request_single_byte(MT6701_ADDRESS, 0x03);
  byte slaveByte2 = I2C_request_single_byte(MT6701_ADDRESS, 0x04);

  uint16_t concat = ((slaveByte1 << 6) | (slaveByte2 >> 2));

  return ((float)concat * 360.0) / 16384.0;
}
