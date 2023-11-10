// Control PWM y lectura de velocidad motor con encoder mediante ESP32 

#include <Wire.h>

//Estructura Union
typedef union{
  float number;
  uint8_t bytes[4];
}valor;

// Direcciones I2C
const int MT6701_ADDRESS = 0x06;
const int PCA9548A_ADDRESS = 0x70;

// Pines del microcontrolador
const int pinIN1 = 32;
const int pinIN2 = 33;

// Configuracion PWM ESP32
const int PWMfreq = 1000; // 1 kHz
const int PWMChannelIN1_0 = 0;
const int PWMChannelIN2_0 = 1;
const int PWMResolution = 16;
const int MAX_DUTY_CYCLE = (int)(pow(2, PWMResolution)-1);

// Parametros del motor
// const float MAX_VEL_MOTOR = 5.752414; // velocidad maxima positiva en rad/s 28GP-385 53RPM
// const float MAX_VEL_MOTOR = 2.575102; // velocidad maxima positiva en rad/s 28GP-385 25RPM
const float MAX_VEL_MOTOR = 3.140995; // velocidad maxima positiva en rad/s JGY
const float ZONA_MUERTA = 0.0; 
const float MAX_POS = 2*PI; // 360.0: grados / 2 * PI: radianes

// Variables globales
float w = 0.0;
float Pos = 0.0;
float Pos_1 = 0.0;
float Pos_real_1 = 0.0;
float Pos_real = 0.0;
int offset = 0;
unsigned long lastTime = 0; // Tiempo anterior
unsigned long sampleTime = 20; // Tiempo de muestreo
//Variable Union
valor PosUnion;
float PWMvalue = 0.0;

void setup(){
  Serial.begin(115200);
  Wire.begin();
  // Se configuran los pines de salida
  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);

  // Se configuran los canales PWM para la ESP32
  ledcSetup(PWMChannelIN1_0, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_0, PWMfreq, PWMResolution);

  ledcAttachPin(pinIN1, PWMChannelIN1_0);
  ledcAttachPin(pinIN2, PWMChannelIN2_0);
  
  PCA9548A_cambio_direccion(0, 1);
  lastTime = millis();
}

void loop(){

  if(millis() - lastTime >= sampleTime){
    if(Serial.available() > 0){
      PWMvalue = recepcion();
      setMotor(PWMvalue, PWMChannelIN1_0, PWMChannelIN2_0);
    }
    Pos_1 = Pos;
    Pos = leerMT6701();

    if( (Pos>(MAX_POS*0.8)) && (Pos_1<(MAX_POS*0.2)) ) offset--;
    if( (Pos<(MAX_POS*0.2)) && (Pos_1>(MAX_POS*0.8)) ) offset++;
    
    Pos_real_1 = Pos_real;
    Pos_real = Pos + offset*MAX_POS;

    //w = (Pos_real-Pos_real_1)*1000.0/(millis()-lastTime); // Velocidad en rads/s
    
    //float wPercentage = mapFloat(w,-MAX_VEL_MOTOR,MAX_VEL_MOTOR,-100,100);
    
    PosUnion.number = Pos_real;
    Serial.write('V');
    for(int i=0; i<4; i++){
      Serial.write(PosUnion.bytes[i]);
      }
    Serial.write('\n');

    lastTime = millis();
  }
}

//Recibir Flotante
float recepcion(){
  int i;
  valor buf;
  for(i=0; i<4; i++)
    buf.bytes[i] = Serial.read();  

  return buf.number;
}

// Funcion para multiplexor I2C
void PCA9548A_cambio_direccion(uint8_t _channel, bool _on_off) {
  Wire.beginTransmission(PCA9548A_ADDRESS);
  Wire.write(_on_off ? (0x01 << _channel) : 0x00);
  Wire.endTransmission();
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

// Configuracion del motor
void setMotor(float valPWM, int IN1, int IN2){
  bool dir = true;
  if(valPWM==0) ledcWrite(IN1, 0), ledcWrite(IN2, 0);
  else {
    if(valPWM<0) dir = false;
    valPWM = abs(valPWM);
    if(valPWM>100) valPWM = 100;
    if(valPWM<ZONA_MUERTA) valPWM = ZONA_MUERTA;
    int dutyCycle = map(valPWM, 0, 100, 0, MAX_DUTY_CYCLE);
    // dir : true = ccw, false = cw
    if(dir) ledcWrite(IN1, dutyCycle), ledcWrite(IN2, 0);
    else ledcWrite(IN1, 0), ledcWrite(IN2, dutyCycle);
  }
}

// Funcion para leer en radianes el encoder magnetico
float leerMT6701() {
  byte slaveByte1 = I2C_request_single_byte(MT6701_ADDRESS, 0x03);
  byte slaveByte2 = I2C_request_single_byte(MT6701_ADDRESS, 0x04);

  uint16_t concat = ((slaveByte1 << 6) | (slaveByte2 >> 2));

  return ((float)concat * MAX_POS) / 16384.0;
}

// Mapeo float
float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}