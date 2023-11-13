#include <Wire.h>

/* Elaboro: Saul Asis Cuevas Morales
            Luis Fernando Morales Flores 
*/
/*           PINOUT ESP32 38 PINES
               _________________
 X      3.3V  |                 |GND        X
        EN    |                 |GPIO23     X
 -      GPIO36|                 |GPIO22 SCL X
 -      GPIO39|                 |GPIO1      -
 -      GPIO34|                 |GPIO3      -
 -      GPIO35|                 |GPIO21 SDA X
 X      GPIO32|                 |GND
 X      GPIO33|                 |GPIO19     X
 X      GPIO25|                 |GPIO18     X
 X      GPIO26|                 |GPIO5      X
 X      GPIO27|                 |GPIO17     X
 X      GPIO14|                 |GPIO16     X
 -      GPIO12|                 |GPIO4      X
        GND   |                 |GPIO0      -
 X      GPIO13|                 |GPIO2      X
 -      GPIO9 |                 |GPIO15     X
 -      GPIO10|                 |GPIO8      -
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
const int dataLength = 9; // Ex: M123 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567

// Pines ESP32
const int pinIN1[7] = {32, 25, 27, 15,  4, 17, 18} ;
const int pinIN2[7] = {33, 26, 14,  2, 16,  5, 19};
const int pinLIMIT_SW = 13;
const int pin3_VIAS = 23;

// Configuracion PWM ESP32
const int PWMfreq = 1000; // 1 kHz
const int PWMChannelIN1_0 = 0;
const int PWMChannelIN2_0 = 1;
const int PWMChannelIN1_1 = 2;
const int PWMChannelIN2_1 = 3;
const int PWMChannelIN1_2 = 4;
const int PWMChannelIN2_2 = 5;
const int PWMChannelIN1_3 = 6;
const int PWMChannelIN2_3 = 7;
const int PWMChannelIN1_4 = 8;
const int PWMChannelIN2_4 = 9;
const int PWMChannelIN1_5 = 10;
const int PWMChannelIN2_5 = 11;
const int PWMChannelIN1_6 = 12;
const int PWMChannelIN2_6 = 13;
const int PWMResolution = 16;
const int MAX_DUTY_CYCLE = (int)(pow(2, PWMResolution)-1);

// Parametros del motor
const float ZONA_MUERTA = 8.0; // Porcentaje PWM en donde se vence la zona muerta
const float MAX_POS = 2*PI;
float B = 3.310322593720104; // Constante de amortiguamiento
float J = 0.085702607785979; // Constante de inercia
float qd = 0.0;
float dqd = 0.0;
float d2qd = 0.0;

// Variables globales
float args[dataLength];
float SetPoints[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
int offset[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float PWMvalue[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
bool flag_mostrar_valores_PID = false;
bool flag_control_M1 = false;
bool flag_control_M2 = false;
bool flag_control_M3 = false;
bool flag_control_M4 = false;
bool flag_control_M5 = false;
bool flag_control_M6 = false;
bool flag_control_M7 = false;
bool busy = false;
bool lastbusy = false;

// Parametros del PID
/*
const float Kp = 19.071;
const float Ki = 49.5756;
const float Kd = 0.50026;
*/

const float T = 5.0/1000.0;
// const float Kp = 1412.13; // 28GP-385 25RPM
// const float Ki = 0.0; // 28GP-385 25RPM
// const float Kd = 68.2507; // 28GP-385 25RPM
const float Kp = 865.5567; // JGY
const float Ki = 0.0; // JGY
const float Kd = 57.3356; // JGY
const float K1 = Kp + Ki*T/2 + Kd/T;
const float K2 = -Kp + Ki*T/2 - 2*Kd/T;
const float K3 = Kd/T;

/*
const float Kp = 1.5308;
const float Ki = 74.8949;
const float Kd = 0.0;
*/
const float error_min = 0.01;

// Variables del PID
float error[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float error_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorI[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorD[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

float z_2[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float z_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float z[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float u_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float u[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

void setup() {
  // Se configuran los pines de salida
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
  ledcSetup(PWMChannelIN1_0, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_0, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_1, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_1, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_2, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_2, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_3, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_3, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_4, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_4, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_5, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_5, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN1_6, PWMfreq, PWMResolution);
  ledcSetup(PWMChannelIN2_6, PWMfreq, PWMResolution);

  // Se vinculan los canales PWM con los pines de salida
  ledcAttachPin(pinIN1[0], PWMChannelIN1_0);
  ledcAttachPin(pinIN2[0], PWMChannelIN2_0);
  ledcAttachPin(pinIN1[1], PWMChannelIN1_1);
  ledcAttachPin(pinIN2[1], PWMChannelIN2_1);
  ledcAttachPin(pinIN1[2], PWMChannelIN1_2);
  ledcAttachPin(pinIN2[2], PWMChannelIN2_2);
  ledcAttachPin(pinIN1[3], PWMChannelIN1_3);
  ledcAttachPin(pinIN2[3], PWMChannelIN2_3);
  ledcAttachPin(pinIN1[4], PWMChannelIN1_4);
  ledcAttachPin(pinIN2[4], PWMChannelIN2_4);
  ledcAttachPin(pinIN1[5], PWMChannelIN1_5);
  ledcAttachPin(pinIN2[5], PWMChannelIN2_5);
  ledcAttachPin(pinIN1[6], PWMChannelIN1_6);
  ledcAttachPin(pinIN2[6], PWMChannelIN2_6);

  Wire.begin();
  Serial.begin(115200);
}

void loop() {
  if(millis() - lastTime >= sampleTime){
    sinewave(2, 0.5);
    // Si una o mas banderas de control estan activadas, el robot
    // esta ocupado y no puede recibir una nueva instruccion
    /*lastbusy = busy;
    busy = flag_control_M1 | flag_control_M2 | flag_control_M3 | flag_control_M4 | flag_control_M5 | flag_control_M6;
    if ( (busy ~= lastbusy) & (~busy) ){
      Serial.println("ready");
    }*/
    if (strComplete) {
      descifrar_comando();
      str = "";
      strComplete = false;
    }
    // Control individual de cada motor
    // Motor Delta 1
    if(flag_control_M1){
      PCA9548A_cambio_direccion(0,1);
      angulo_1[0]= angulo[0];
      angulo[0] = leerMT6701();
      if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
      if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;

      angulo_real_1[0] = angulo_real[0];
      angulo_real[0] = angulo[0] + offset[0]*MAX_POS;
      // PWMvalue[0] = calcularPID2(0, SetPoints[0], angulo_real[0]);
      PWMvalue[0] = calcularPIDFF(0, qd, dqd, d2qd, angulo_real[0]);
      setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      /*
      if(abs(error[0])<error_min){
        PWMvalue[0] = 0.0;
        setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M1 = false;
      }
      else setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      */
    }
    // Motor Delta 2
    if(flag_control_M2){
      PCA9548A_cambio_direccion(1,1);
      angulo[1] = leerMT6701();
      PWMvalue[1] = calcularPID(1, SetPoints[1], angulo[1]);
      if(abs(error[1])<error_min){
        PWMvalue[1] = 0.0;
        setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M2 = false;
      }
      else setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
    }
    // Motor Delta 3
    if(flag_control_M3){
      PCA9548A_cambio_direccion(2,1);
      angulo[2] = leerMT6701();
      PWMvalue[2] = calcularPID(2, SetPoints[2], angulo[2]);
      if(abs(error[2])<error_min){
        PWMvalue[2] = 0.0;
        setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M3 = false;
      }
      else setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
    }
    // Motor Manipulador
    if(flag_control_M4){
      PCA9548A_cambio_direccion(3,1);
      angulo[3] = leerMT6701();
      PWMvalue[3] = calcularPID(3, SetPoints[3], angulo[3]);
      if(abs(error[3])<error_min){
        PWMvalue[3] = 0.0;
        setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M4 = false;
      }
      else setMotor(PWMvalue[3], PWMChannelIN1_3, PWMChannelIN2_3);
    }
    // Motor Dispensador
    if(flag_control_M5){
      // Falta mandar el pulso
      /*
      PCA9548A_cambio_direccion(4,1);
      angulo[4] = leerMT6701();
      PWMvalue[4] = calcularPID(4, SetPoints[4], angulo[4]);
      if(abs(error[4])<error_min){
        PWMvalue[4] = 0.0;
        setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M5 = false;
      }
      else setMotor(PWMvalue[4], PWMChannelIN1_4, PWMChannelIN2_4);
      */
      flag_control_M5 = false;
    }
    // Motor cambio de Herramienta
    if(flag_control_M6){
      PCA9548A_cambio_direccion(5,1);
      angulo[5] = leerMT6701();
      PWMvalue[5] = calcularPID(5, SetPoints[5], angulo[5]);
      if(abs(error[5])<error_min){
        PWMvalue[5] = 0.0;
        setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M6 = false;
      }
      else setMotor(PWMvalue[5], PWMChannelIN1_5, PWMChannelIN2_5);
    }
    // Motor Inventario
    if(flag_control_M7){
      PCA9548A_cambio_direccion(6,1);
      angulo[6] = leerMT6701();
      PWMvalue[6] = calcularPID(6, SetPoints[6], angulo[6]);
      if(abs(error[6])<error_min){
        PWMvalue[6] = 0.0;
        setMotor(0.0, PWMChannelIN1_6, PWMChannelIN2_6);
        PCA9548A_cambio_direccion(0,0);
        flag_control_M7 = false;
      }
      else setMotor(PWMvalue[6], PWMChannelIN1_6, PWMChannelIN2_6);
    }
    // Muestra los valores para monitorear el comportamiento del PID
    if(flag_mostrar_valores_PID){      
      // Serial.print("PosRef:"); Serial.print(SetPoints[0],5); Serial.print(",");
      Serial.print("PosRef:"); Serial.print(qd,5); Serial.print(",");
      Serial.print("Pos:"); Serial.print(angulo_real[0],5); Serial.print(",");
      Serial.print("Error:"); Serial.print(error[0],5); Serial.print(",");
      Serial.print("PID:"); Serial.println(PWMvalue[0],5);
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
  // Serial.print("Arg4: "), Serial.println(args[3]);
  // Serial.print("Arg5: "), Serial.println(args[4]);
  // Serial.print("Arg6: "), Serial.println(args[5]);
  // Serial.print("Arg7: "), Serial.println(args[6]);
  // Serial.print("Arg8: "), Serial.println(args[7]);
  // Serial.print("Arg9: "), Serial.println(args[8]);

  switch(comm1) {
    // Mover un motor a la posicion deseada
    // Ej: M4 120.5
    // Ej: M123 12.3 45.6 78.9
    case 'M':
      //Serial.print("Quieres mover el motor "), Serial.println(comm2.toInt());
      switch(comm2.toInt()) {
        case 123:
          flag_control_M1 = true;
          SetPoints[0] = args[0];
          SetPoints[1] = args[1];
          SetPoints[2] = args[2];
          break;
        case 1:
          flag_control_M1 = true;
          SetPoints[0] = args[0];
          break;
        case 2:
          flag_control_M2 = true;
          SetPoints[1] = args[0];
          break;
        case 3:
          flag_control_M3 = true;
          SetPoints[2] = args[0];
          break;
        case 4:
          flag_control_M4 = true;
          SetPoints[3] = args[0];
          break;
        case 5:
          flag_control_M5 = true;
          SetPoints[4] = args[0];
          break;
        case 6:
          flag_control_M6 = true;
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
    // STOP
    case '-':
      setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
      setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
      setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
      setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
      setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
      setMotor(0.0, PWMChannelIN1_6, PWMChannelIN2_6);

      flag_control_M1 = false;
      flag_control_M2 = false;
      flag_control_M3 = false;
      flag_control_M4 = false;
      flag_control_M5 = false;
      flag_control_M6 = false;
      break;
    case 'B':
      B = args[0];
      break;
    case 'J':
      J = args[0];
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

  return ((float)concat * MAX_POS) / 16384.0;
}

// Calcular PID
float calcularPID(int motor, float setpoint, float input){
  error[motor] = setpoint-input; // Error actual

  errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
  errorD[motor] = (error[motor]-error_1[motor])/(sampleTime*0.001); // Error derivativo
  error_1[motor] = error[motor]; // Error anterior
  
  return Kp*error[motor]+Ki*errorI[motor]+Kd*errorD[motor];
}

// Calcular PID
float calcularPID2(int motor, float setpoint, float input){
  z_2[motor] = z_1[motor];
  z_1[motor] = z[motor];
  z[motor] = setpoint - input;
  error[motor] = z[motor];

  u_1[motor] = u[motor];
  u[motor] = K1*z[motor] + K2*z_1[motor] + K3*z_2[motor] + u_1[motor];
  return u[motor];
}

// Calcular PID con prealimentacion (feed-forward)
float calcularPIDFF(int motor, float qd, float dqd, float d2qd, float q){
  // qd   : pos deseada (trayectoria)
  // dqd  : vel deseada (trayectoria)
  // d2qd : acel deseada (trayectoria)
  // q    : pos real (medida)
  error[motor] = q-qd; // Error actual
  errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
  error_1[motor] = error[motor]; // Error anterior
  return J*d2qd + B*dqd - J*( Kp*error[motor] + Ki*errorI[motor] + Kd*(error[motor] - error_1[motor])/(sampleTime*0.001) );
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

// Funcion seno para prueba de trayectoria
void sinewave(float A, float w){
  float t = millis()/1000.0;
  qd = A*sin(w*t);
  dqd = w*A*sin(w*t+PI/2);
  d2qd = -pow(w,2)*A*sin(w*t);
}
