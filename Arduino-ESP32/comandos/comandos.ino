#include <Wire.h>

/* Elaboró: Saúl Asís Cuevas Morales
            Luis Fernando Morales Flores 
*/
/*           PINOUT ESP32 38 PINES
               _________________
        3.3V  |                 |GND
        EN    |                 |GPIO23
 X      GPIO36|                 |GPIO22 SCL X
 X      GPIO39|                 |GPIO1
 X      GPIO34|                 |GPIO3
 X      GPIO35|                 |GPIO21 SDA X
 X      GPIO32|                 |GND
 X      GPIO33|                 |GPIO19     X
 X      GPIO25|                 |GPIO18
 X      GPIO26|                 |GPIO5
 X      GPIO27|                 |GPIO17
 X      GPIO14|                 |GPIO16     X
 X      GPIO12|                 |GPIO4      X
        GND   |                 |GPIO0      X
 X      GPIO13|                 |GPIO2      X
 X      GPIO9 |                 |GPIO15     X
 X      GPIO10|                 |GPIO8      X
 X      GPIO11|       ___       |GPIO7      X
        5V    |______||_||______|GPIO6      X
*/

// Direcciones I2C
const int MT6701_ADDRESS = 0x06;
const int PCA9548A_ADDRESS = 0x70;

// Tiempo de muestreo
unsigned long lastTime = 0; // Tiempo anterior
unsigned long sampleTime = 5; // Tiempo de muestreo en milisegundos

// Configuracion lectura de datos serial
String str = "";        // String recibida por el microcontrolador
bool strComplete = false;  // bandera de identificacion de String
const char separator = ' ';
const int dataLength = 3;

// Pines ESP32
const int pinPWM[7] = {36, 35, 25, 14,  9,  6, 15};
const int pinIN1[7] = {39, 32, 26, 12, 10,  7,  2};
const int pinIN2[7] = {34, 33, 27, 13, 11,  8,  0};
const int pinLIMIT_SW = 4;
const int pin3_VIAS = 16;

// Configuracion PWM ESP32
//const int PWMfreq = 1000; // 1 kHz
//const int PWMChannel = 0;
const int PWMResolution = 8;
const int MAX_DUTY_CYCLE = (int)(pow(2, PWMResolution)-1);

// Parametros del motor
const float ZONA_MUERTA = 20; // Porcentaje PWM en donde se vence la zona muerta

// Variables globales
float args[dataLength];
float angulo[6];
float PWMvalue[6];
bool flag_mostrar_valores_PID = false;
bool flag_control_M1 = false;
bool flag_control_M2 = false;
bool flag_control_M3 = false;
bool flag_control_M4 = false;
bool flag_control_M5 = false;
bool flag_control_M6 = false;

// Parametros del PID
const float Kp = 4.249;
const float Ki = 0.14678;
const float Kd = 2.4281e-06;
const float error_min = 0.01;

// Variables del PID
float error[6];
float error_1[6];
float errorI[6];
float errorD[6];

void setup() {
  Wire.begin();
  Serial.begin(115200);
}

void loop() {
  if(millis() - lastTime >= sampleTime){
    if (strComplete) {
      descifrar_comando();
      str = "";
      strComplete = false;
    }
    if(flag_control_M1 && flag_control_M2 && flag_control_M3){
      PCA9548A_cambio_direccion(0,1);
      angulo[0] = leerMT6701();
      PWMvalue[0] = calcularPID(0, args[0], angulo[0]);
      setMotor(PWMvalue[0], pinPWM[0], pinIN1[0], pinIN2[0]);

      PCA9548A_cambio_direccion(1,1);
      angulo[1] = leerMT6701();
      PWMvalue[1] = calcularPID(1, args[1], angulo[1]);
      setMotor(PWMvalue[1], pinPWM[1], pinIN1[1], pinIN2[1]);

      PCA9548A_cambio_direccion(2,1);
      angulo[2] = leerMT6701();
      PWMvalue[2] = calcularPID(2, args[2], angulo[2]);
      setMotor(PWMvalue[2], pinPWM[2], pinIN1[2], pinIN2[2]);

      if(error[0]<error_min && error[1]<error_min && error[2]<error_min){
        flag_control_M1 = false, flag_control_M2 = false, flag_control_M3 = false;
        PCA9548A_cambio_direccion(0,0);
      }
    }
    else{
      if(flag_control_M1){
        PCA9548A_cambio_direccion(0,1);
        angulo[0] = leerMT6701();
        PWMvalue[0] = calcularPID(0, args[0], angulo[0]);
        setMotor(PWMvalue[0], pinPWM[0], pinIN1[0], pinIN2[0]);
        if(error[0]<error_min){
          flag_control_M1 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
      if(flag_control_M2){
        PCA9548A_cambio_direccion(1,1);
        angulo[1] = leerMT6701();
        PWMvalue[1] = calcularPID(1, args[1], angulo[1]);
        setMotor(PWMvalue[1], pinPWM[1], pinIN1[1], pinIN2[1]);
        if(error[1]<error_min){
          flag_control_M2 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
      if(flag_control_M3){
        PCA9548A_cambio_direccion(2,1);
        angulo[2] = leerMT6701();
        PWMvalue[2] = calcularPID(2, args[2], angulo[2]);
        setMotor(PWMvalue[2], pinPWM[2], pinIN1[2], pinIN2[2]);
        if(error[2]<error_min){
          flag_control_M3 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
      if(flag_control_M4){
        PCA9548A_cambio_direccion(3,1);
        angulo[3] = leerMT6701();
        PWMvalue[3] = calcularPID(3, args[3], angulo[3]);
        setMotor(PWMvalue[3], pinPWM[3], pinIN1[3], pinIN2[3]);
        if(error[3]<error_min){
          flag_control_M4 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
      if(flag_control_M5){
        PCA9548A_cambio_direccion(4,1);
        angulo[4] = leerMT6701();
        PWMvalue[4] = calcularPID(4, args[4], angulo[4]);
        setMotor(PWMvalue[4], pinPWM[4], pinIN1[4], pinIN2[4]);
        if(error[4]<error_min){
          flag_control_M5 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
      if(flag_control_M6){
        PCA9548A_cambio_direccion(5,1);
        angulo[5] = leerMT6701();
        PWMvalue[5] = calcularPID(5, args[5], angulo[5]);
        setMotor(PWMvalue[5], pinPWM[5], pinIN1[5], pinIN2[5]);
        if(error[5]<error_min){
          flag_control_M6 = false;
          PCA9548A_cambio_direccion(0,0);
        }
      }
    }

    if(flag_mostrar_valores_PID){
      Serial.print("PosRef:"); Serial.print(args[0]); Serial.print(",");
      Serial.print("Pos:"); Serial.print(angulo[0]); Serial.print(",");
      Serial.print("Error:"); Serial.print(error[0]); Serial.print(",");
      Serial.print("PID:"); Serial.println(PWMvalue[0]);
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

// Funcion para descifrar el comando recibido por comunicacion serial
// Ej: M4 120.5, significa mover el motor 4 a la posicion 120.5 grados 
void descifrar_comando(){
  str = str.substring(0, str.indexOf("\n"));

  int index = str.indexOf(separator);
  char comm1 = str.charAt(0);
  String comm2 = str.substring(1, index);
  str = str.substring(index+1);

  for(int i=0; i<dataLength; i++){
      index = str.indexOf(separator); // Busca el indice del separador en el string recibido
      args[i]=str.substring(0, index).toFloat();
      str = str.substring(index+1);
    }

  Serial.print("Comando: "), Serial.print(comm1), Serial.print(" "), Serial.println(comm2);
  Serial.print("Arg1: "), Serial.println(args[0]);
  Serial.print("Arg2: "), Serial.println(args[1]);
  Serial.print("Arg3: "), Serial.println(args[2]);

  switch(comm1) {
    // Mover un motor a la posicion deseada
    // Ej: M4 120.5
    // Ej: M123 12.3 45.6 78.9
    case 'M':
      //Serial.print("Quieres mover el motor "), Serial.println(comm2.toInt());
      switch(comm2.toInt()) {
        case 123:
          break;
        case 1:
          flag_control_M1 = true;
          break;
        case 2:
          flag_control_M2 = true;
          break;
        case 3:
          flag_control_M3 = true;
          break;
        case 4:
          flag_control_M4 = true;
          break;
        case 5:
          flag_control_M5 = true;
          break;
        case 6:
          flag_control_M6 = true;
          break;
        case 7:
          // Mandar un pulso de activacion por lo que dure arg1
          break;
        default:
          Serial.println("No existe ese motor");
          break;
      }
      break;
    // Leer todos los encoders del robot delta
    // Ej: E
    case 'E':
      //Serial.println("Quieres leer los encoders");
      PCA9548A_cambio_direccion(0, 1);
      Serial.print(leerMT6701()), Serial.print(" ");
      PCA9548A_cambio_direccion(1, 1);
      Serial.print(leerMT6701()), Serial.print(" ");
      PCA9548A_cambio_direccion(2, 1);
      Serial.print(leerMT6701()), Serial.print(" ");
      PCA9548A_cambio_direccion(3, 1);
      Serial.print(leerMT6701()), Serial.print(" ");
      PCA9548A_cambio_direccion(4, 1);
      Serial.print(leerMT6701()), Serial.print(" ");
      PCA9548A_cambio_direccion(5, 1);
      Serial.println(leerMT6701());
      PCA9548A_cambio_direccion(0, 0); // reset
      break;
    // HOME a herramienta
    case 'H':
      Serial.println("Quieres hacer subrutina de HOME en la herramienta");
      break;
    // Encender o apagar la valvula de tres vias
    case 'V':
      if( comm2.toInt() ) digitalWrite(pin3_VIAS, HIGH), Serial.println("Valvula encendida");
      else digitalWrite(pin3_VIAS, LOW), Serial.println("Valvula apagada");
      break;
    case 'X':
      if( comm2.toInt() ) flag_mostrar_valores_PID = true;
      else flag_mostrar_valores_PID = false;
      break;
    default:
      Serial.println("No reconozco ese comando");
      break;
  }
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

// Funcion para leer en grados el encoder magnetico
float leerMT6701() {
  byte slaveByte1 = I2C_request_single_byte(MT6701_ADDRESS, 0x03);
  byte slaveByte2 = I2C_request_single_byte(MT6701_ADDRESS, 0x04);

  uint16_t concat = ((slaveByte1 << 6) | (slaveByte2 >> 2));

  return ((float)concat * 360.0) / 16384.0;
}

// Calcular PID
float calcularPID(int motor, float setpoint, float input){
  error[motor] = setpoint-input; // Error actual

  errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
  errorD[motor] = (error[motor]-error_1[motor])/(sampleTime*0.001); // Error derivativo
  error_1[motor] = error[motor]; // Error anterior
  
  return Kp*error[motor]+Ki*errorI[motor]+Kd*errorD[motor];
}

// Configuracion del motor
void setMotor(float valPWM, int channelPWM, int IN1, int IN2){
  bool dir = true;
  if(valPWM<0) dir = false;
  valPWM = abs(valPWM);
  if(valPWM>100) valPWM = 100;
  if(valPWM<ZONA_MUERTA) valPWM = ZONA_MUERTA;
  int dutyCycle = map(valPWM, 0, 100, 0, MAX_DUTY_CYCLE);
  //ledcWrite(channelPWM, dutyCycle);
  analogWrite(channelPWM, dutyCycle);
  // dir : true = ccw, false = cw
  if(dir) digitalWrite(IN1, HIGH), digitalWrite(IN2, LOW);
  else digitalWrite(IN1, LOW), digitalWrite(IN2, HIGH);
}
