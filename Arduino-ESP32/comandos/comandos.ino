#include <Wire.h>

/* Elaboro: Saul Asis Cuevas Morales
            Luis Fernando Morales Flores 
*/
/*           PINOUT ESP32 38 PINES
               _________________
 X      3.3V  |                 |GND        X
        EN    |                 |GPIO23
 X      GPIO36|                 |GPIO22 SCL X
 X      GPIO39|                 |GPIO1      X
 X      GPIO34|                 |GPIO3      X
 X      GPIO35|                 |GPIO21 SDA X
 X      GPIO32|                 |GND
 X      GPIO33|                 |GPIO19     X
 X      GPIO25|                 |GPIO18     X
 X      GPIO26|                 |GPIO5      X
 X      GPIO27|                 |GPIO17     X
 X      GPIO14|                 |GPIO16     X
 X      GPIO12|                 |GPIO4      X
        GND   |                 |GPIO0      X
 X      GPIO13|                 |GPIO2      X
 -      GPIO9 |                 |GPIO15     X
 ~      GPIO10|                 |GPIO8      -
 -      GPIO11|       ___       |GPIO7      -
        5V    |______||_||______|GPIO6      -
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
const int pinPWM[7] = {36, 35, 25, 14, 15,  4, 5};
const int pinIN1[7] = {39, 32, 26, 12,  2, 16, 18} ;
const int pinIN2[7] = {34, 33, 27, 13,  0, 17, 19};
const int pinLIMIT_SW = 1;
const int pin3_VIAS = 3;

// Configuracion PWM ESP32
const int PWMfreq = 1000; // 1 kHz
const int PWMChannel0 = 0;
const int PWMChannel1 = 0;
const int PWMChannel2 = 0;
const int PWMChannel3 = 0;
const int PWMChannel4 = 0;
const int PWMChannel5 = 0;
const int PWMChannel6 = 0;
const int PWMResolution = 16;
const int MAX_DUTY_CYCLE = (int)(pow(2, PWMResolution)-1);

// Parametros del motor
const float ZONA_MUERTA = 30.0; // Porcentaje PWM en donde se vence la zona muerta

// Variables globales
float args[dataLength];
float SetPoints[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float PWMvalue[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
bool flag_mostrar_valores_PID = false;
bool flag_control_M123 = false;
bool flag_control_M1 = false;
bool flag_control_M2 = false;
bool flag_control_M3 = false;
bool flag_control_M4 = false;
bool flag_control_M5 = false;
bool flag_control_M6 = false;
bool busy = false;

// Parametros del PID
const float Kp = 4.249;
const float Ki = 0.14678;
const float Kd = 2.4281e-06;
const float error_min = 0.5;

// Variables del PID
float error[6];
float error_1[6];
float errorI[6];
float errorD[6];

void setup() {
  // Se configuran los pines de salida
  pinMode(pinPWM[0], OUTPUT);
  pinMode(pinPWM[1], OUTPUT);
  pinMode(pinPWM[2], OUTPUT);
  pinMode(pinPWM[3], OUTPUT);
  pinMode(pinPWM[4], OUTPUT);
  pinMode(pinPWM[5], OUTPUT);
  pinMode(pinPWM[6], OUTPUT);

  pinMode(pinIN1[0], OUTPUT);
  pinMode(pinIN1[1], OUTPUT);
  pinMode(pinIN1[2], OUTPUT);
  pinMode(pinIN1[3], OUTPUT);
  pinMode(pinIN1[4], OUTPUT);
  pinMode(pinIN1[5], OUTPUT);
  pinMode(pinIN1[6], OUTPUT);

  pinMode(pinIN2[0], OUTPUT);
  pinMode(pinIN2[1], OUTPUT);
  pinMode(pinIN2[2], OUTPUT);
  pinMode(pinIN2[3], OUTPUT);
  pinMode(pinIN2[4], OUTPUT);
  pinMode(pinIN2[5], OUTPUT);
  pinMode(pinIN2[6], OUTPUT);

  pinMode(pinLIMIT_SW, OUTPUT);
  pinMode(pin3_VIAS, OUTPUT);

  // Se configuran los canales PWM para la ESP32
  ledcSetup(PWMChannel0, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel1, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel2, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel3, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel4, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel5, PWMfreq, PWMResolution);
  ledcSetup(PWMChannel6, PWMfreq, PWMResolution);

  // Se vinculan los canales PWM con los pines de salida
  ledcAttachPin(pinPWM[0], PWMChannel0);
  ledcAttachPin(pinPWM[1], PWMChannel1);
  ledcAttachPin(pinPWM[2], PWMChannel2);
  ledcAttachPin(pinPWM[3], PWMChannel3);
  ledcAttachPin(pinPWM[4], PWMChannel4);
  ledcAttachPin(pinPWM[5], PWMChannel5);
  ledcAttachPin(pinPWM[6], PWMChannel6);

  Wire.begin();
  Serial.begin(115200);
}

void loop() {
  if(millis() - lastTime >= sampleTime){
    // Si una o mas banderas de control estan activadas, el robot
    // esta ocupado y no puede recibir una nueva instruccion
    busy = flag_control_M123 | flag_control_M1 | flag_control_M2 | flag_control_M3 | flag_control_M4 | flag_control_M5 | flag_control_M6;
    if (strComplete) {
      descifrar_comando();
      str = "";
      strComplete = false;
    }
    // Control de los motores en conjunto del robot delta
    if(flag_control_M123){
      if(error[0]<error_min){
          flag_control_M1 = false;
          PWMvalue[0] = 0;
          setMotor(PWMvalue[0], PWMChannel0, pinIN1[0], pinIN2[0]);
          PCA9548A_cambio_direccion(0,0);
        }
      if(error[1]<error_min){
          flag_control_M2 = false;
          PWMvalue[1] = 0;
          setMotor(PWMvalue[1], PWMChannel1, pinIN1[1], pinIN2[1]);
          PCA9548A_cambio_direccion(0,0);
        }
      if(error[2]<error_min){
          flag_control_M3 = false;
          PWMvalue[2] = 0;
          setMotor(PWMvalue[2], PWMChannel2, pinIN1[2], pinIN2[2]);
          PCA9548A_cambio_direccion(0,0);
        }
      else{
        if(flag_control_M1){
          PCA9548A_cambio_direccion(0,1);
          angulo[0] = leerMT6701();
          PWMvalue[0] = calcularPID(0, SetPoints[0], angulo[0]);
          setMotor(PWMvalue[0], PWMChannel0, pinIN1[0], pinIN2[0]);
          }

        if(flag_control_M2){
          PCA9548A_cambio_direccion(1,1);
          angulo[1] = leerMT6701();
          PWMvalue[1] = calcularPID(1, SetPoints[1], angulo[1]);
          setMotor(PWMvalue[1], PWMChannel1, pinIN1[1], pinIN2[1]);
          }

        if(flag_control_M3){
          PCA9548A_cambio_direccion(2,1);
          angulo[2] = leerMT6701();
          PWMvalue[2] = calcularPID(2, SetPoints[2], angulo[2]);
          setMotor(PWMvalue[2], PWMChannel2, pinIN1[2], pinIN2[2]);
          }
        }
      }
    // Control individual de cada motor
    else{
      if(flag_control_M1){
        if(error[0]<error_min){
          flag_control_M1 = false;
          PWMvalue[0] = 0;
          setMotor(PWMvalue[0], PWMChannel0, pinIN1[0], pinIN2[0]);
          PCA9548A_cambio_direccion(0,0);
        }
        else{
          angulo[0] = leerMT6701();
          PWMvalue[0] = calcularPID(0, SetPoints[0], angulo[0]);
          setMotor(PWMvalue[0], PWMChannel0, pinIN1[0], pinIN2[0]);
        }
      }
      if(flag_control_M2){
        if(error[1]<error_min){
          flag_control_M2 = false;
          PWMvalue[1] = 0;
          setMotor(PWMvalue[1], PWMChannel1, pinIN1[1], pinIN2[1]);
          PCA9548A_cambio_direccion(0,0);
        }
        else{
          angulo[1] = leerMT6701();
          PWMvalue[1] = calcularPID(1, SetPoints[1], angulo[1]);
          setMotor(PWMvalue[1], PWMChannel1, pinIN1[1], pinIN2[1]);
        }
      }
      if(flag_control_M3){
        if(error[2]<error_min){
          flag_control_M3 = false;
          PWMvalue[2] = 0;
          setMotor(PWMvalue[2], PWMChannel2, pinIN1[2], pinIN2[2]);
          PCA9548A_cambio_direccion(0,0);
        }
        else{
          angulo[2] = leerMT6701();
          PWMvalue[2] = calcularPID(2, SetPoints[2], angulo[2]);
          setMotor(PWMvalue[2], PWMChannel2, pinIN1[2], pinIN2[2]);
        }
      }
      if(flag_control_M4){
        angulo[3] = leerMT6701();
        PWMvalue[3] = calcularPID(3, SetPoints[3], angulo[3]);
        if(abs(error[3])<error_min){
          PWMvalue[3] = 0.0;
          setMotor(0.0, PWMChannel3, pinIN1[3], pinIN2[3]);
          PCA9548A_cambio_direccion(0,0);
          flag_control_M4 = false;
        }
        else setMotor(PWMvalue[3], PWMChannel3, pinIN1[3], pinIN2[3]);
      }
      if(flag_control_M5){
        if(error[4]<error_min){
          flag_control_M5 = false;
          PWMvalue[4] = 0;
          setMotor(PWMvalue[4], PWMChannel4, pinIN1[4], pinIN2[4]);
          PCA9548A_cambio_direccion(0,0);
        }
        else{
          angulo[4] = leerMT6701();
          PWMvalue[4] = calcularPID(4, SetPoints[4], angulo[4]);
          setMotor(PWMvalue[4], PWMChannel4, pinIN1[4], pinIN2[4]);
        }
      }
      if(flag_control_M6){
        if(error[5]<error_min){
          flag_control_M6 = false;
          PWMvalue[5] = 0;
          setMotor(PWMvalue[5], PWMChannel5, pinIN1[5], pinIN2[5]);
          PCA9548A_cambio_direccion(0,0);
        }
        else{
          angulo[5] = leerMT6701();
          PWMvalue[5] = calcularPID(5, SetPoints[5], angulo[5]);
          setMotor(PWMvalue[5], PWMChannel5, pinIN1[5], pinIN2[5]);
        }
      }
    }
    // Muestra los valores para monitorear el comportamiento del PID
    if(flag_mostrar_valores_PID){
      Serial.print("PosRef:"); Serial.print(SetPoints[3]); Serial.print(",");
      Serial.print("Pos:"); Serial.print(angulo[3]); Serial.print(",");
      Serial.print("Error:"); Serial.print(error[3]); Serial.print(",");
      Serial.print("PID:"); Serial.println(PWMvalue[3]);
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
          PCA9548A_cambio_direccion(0,1);
          SetPoints[0] = args[0];
          break;
        case 2:
          flag_control_M2 = true;
          PCA9548A_cambio_direccion(1,1);
          SetPoints[1] = args[0];
          break;
        case 3:
          flag_control_M3 = true;
          PCA9548A_cambio_direccion(2,1);
          SetPoints[2] = args[0];
          break;
        case 4:
          flag_control_M4 = true;
          PCA9548A_cambio_direccion(3,1);
          SetPoints[3] = args[0];
          break;
        case 5:
          flag_control_M5 = true;
          PCA9548A_cambio_direccion(4,1);
          SetPoints[4] = args[0];
          break;
        case 6:
          flag_control_M6 = true;
          PCA9548A_cambio_direccion(5,1);
          SetPoints[5] = args[0];
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
  if(valPWM==0) ledcWrite(channelPWM, 0), digitalWrite(IN1, LOW), digitalWrite(IN2, LOW);
  else {
    if(valPWM<0) dir = false;
    valPWM = abs(valPWM);
    if(valPWM>100) valPWM = 100;
    if(valPWM<ZONA_MUERTA) valPWM = ZONA_MUERTA;
    int dutyCycle = map(valPWM, 0, 100, 0, MAX_DUTY_CYCLE);
    ledcWrite(channelPWM, dutyCycle);
    //analogWrite(channelPWM, dutyCycle);
    // dir : true = ccw, false = cw
    if(dir) digitalWrite(IN1, HIGH), digitalWrite(IN2, LOW);
    else digitalWrite(IN1, LOW), digitalWrite(IN2, HIGH);
  }
}
