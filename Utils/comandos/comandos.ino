/*                              Elaboro: Saul Asis Cuevas Morales
                                      Luis Fernando Morales Flores 

                                         PINOUT ESP32 38 PINES
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

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
SINTAXIS: [LETRA][COMANDO SECUNDARIO] [ARGUMENTO 1] [ARGUMENTO 2] [ARGUMENTO 3] ... [ARGUMENTO 9]
COMANDOS DISPONIBLES: 

- M : Movimiento de motor
    123 qd1 dqd1 d2qd1 qd2 dqd2 d2qd2 qd3 dqd3 d2qd3        motores delta
    1 qd                                                    M1 : Motor Delta 1
    2 qd                                                    M2 : Motor Delta 2
    3 qd                                                    M3 : Motor Delta 3
    4 qd                                                    M4 : Manipulador PnP
    5 qd                                                    M5 : Cambio de herramienta
    6 qd                                                    M6 : Inventario

- U : Movimiento de motor por usuario
    1 amplitud periodo
    2 amplitud periodo
    3 amplitud periodo
    4 amplitud periodo
    5 amplitud periodo
    6 amplitud periodo

- S : Dispensar soldadura
    amplitud periodo                                        M7 : Dispensador de soldadura

- E : Lectura de encoders

- H : HOME de herramienta

- T : Seleccion de herramienta
    0                                                       mover motor M5 a pos de Camara
    1                                                       mover motor M5 a pos de Dispensador
    2                                                       mover motor M5 a pos de Manipulador PnP

- V : Valvula
    0                                                       apagar valvula de vacio
    1                                                       encender valvula de vacio

- X : Mostrar los valores del control

- - : Apagar todos los motores

- B : Cambiar el valor de B
    B_                                                      B_ : nuevo valor de B

- J : Cambiar el valor de J
    J_                                                      J_ : nuevo valor de J

- C : Cambiar el valor de la posicion de la herramienta camara
    C_                                                      C_ : nuevo valor de C

- D : Cambiar el valor de la posicion de la herramienta dispensador
    D_                                                      D_ : nuevo valor de D

- P : Cambiar el valor de la posicion de la herramienta manipulador PnP
    P_                                                      P_ : nuevo valor de P
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*/
#include <Wire.h>

// Direcciones I2C
const int MT6701_ADDRESS = 0x06;
const int PCA9548A_ADDRESS = 0x70;
bool i2c_not_present = true;

// Tiempo de muestreo
unsigned long lastTime = 0; // Tiempo anterior
unsigned long sampleTime = 5; // Tiempo de muestreo en milisegundos

// Configuracion lectura de datos serial
String str = "";        // String recibida por el microcontrolador
bool strComplete = false;  // bandera de identificacion de String
const char separator = ' ';
const int dataLength = 9; // Ex: M123 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567

// Pines ESP32
const int pinIN1[7] = {32, 25, 27, 15,  4, 17, 18};
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
float qds[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float dqds[3] = {0.0, 0.0, 0.0}; // Solo se usa para M1, M2 y M3
float d2qds[3] = {0.0, 0.0, 0.0}; // Solo se usa para M1, M2 y M3
float angulo[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
int offset[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float PWMvalue[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float amplitud = 0.0;
float periodo = 0.0;
bool flag_mostrar_valores_PID = false;
bool flag_HOME_realizado = false;
bool flag_control_M1 = false;
bool flag_control_M2 = false;
bool flag_control_M3 = false;
bool flag_control_M4 = false;
bool flag_control_M5 = false;
bool flag_control_M6 = false;
bool flag_control_M123 = false;

// Homing y herramienta
float pos_home_herr = 0.0;
const float vel_alta = 80.0;
const float vel_baja = 20.0;
const float max_pos_herr = 100.0;
const float min_pos_herr = -100.0;
float pos_herramienta_0 = 0.0;
float pos_herramienta_1 = 0.0;
float pos_herramienta_2 = 0.0;

// Parametros del PID
const float error_min = 0.001;
const float T = 5.0/1000.0;
// const float Kp = 1412.13; // 28GP-385 25RPM
// const float Ki = 0.0; // 28GP-385 25RPM
// const float Kd = 68.2507; // 28GP-385 25RPM
// const float Kp = 865.5567; // JGY
// const float Ki = 0.0; // JGY
// const float Kd = 57.3356; // JGY
// const float K1 = Kp + Ki*T/2 + Kd/T;
// const float K2 = -Kp + Ki*T/2 - 2*Kd/T;
// const float K3 = Kd/T;

const float Kp[6] = {1412.13, 1412.13, 1412.13, 0.0, 865.5567, 865.5567};
const float Ki[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
const float Kd[6] = {68.2507, 68.2507, 68.2507, 0.0, 57.3356, 57.3356};

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
  Wire.setTimeout(1);
  PCA9548A_cambio_direccion(0,1);
  angulo_real[0] = leerMT6701();
  PCA9548A_cambio_direccion(1,1);
  angulo_real[1] = leerMT6701();
  PCA9548A_cambio_direccion(2,1);
  angulo_real[2] = leerMT6701();
  PCA9548A_cambio_direccion(3,1);
  angulo_real[3] = leerMT6701();
  PCA9548A_cambio_direccion(4,1);
  angulo_real[4] = leerMT6701();
  PCA9548A_cambio_direccion(5,1);
  angulo_real[5] = leerMT6701();
  
  Serial.begin(250000);
}

void loop() {
  if (strComplete) {
      descifrar_comando();
      str = "";
      strComplete = false;
    }
  if(millis() - lastTime >= sampleTime){
    // Control en conjunto de los motores delta
    if(flag_control_M123){
      PCA9548A_cambio_direccion(0,1);
      angulo_1[0]= angulo[0];
      angulo[0] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      else{
        if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
        if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;

        angulo_real_1[0] = angulo_real[0];
        angulo_real[0] = angulo[0] + offset[0]*MAX_POS;
        PWMvalue[0] = calcularPIDFF(0, qds[0], dqds[0], d2qds[0], angulo_real[0]);
        setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      }

      PCA9548A_cambio_direccion(1,1);
      angulo_1[1]= angulo[1];
      angulo[1] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      else{
        if( (angulo[1]>(MAX_POS*0.9)) && (angulo_1[1]<(MAX_POS*0.1)) ) offset[1]--;
        if( (angulo[1]<(MAX_POS*0.1)) && (angulo_1[1]>(MAX_POS*0.9)) ) offset[1]++;

        angulo_real_1[1] = angulo_real[1];
        angulo_real[1] = angulo[1] + offset[1]*MAX_POS;
        PWMvalue[1] = calcularPIDFF(1, qds[1], dqds[1], d2qds[1], angulo_real[1]);
        setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
      }

      PCA9548A_cambio_direccion(2,1);
      angulo_1[2]= angulo[2];
      angulo[2] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
      else{
        if( (angulo[2]>(MAX_POS*0.9)) && (angulo_1[2]<(MAX_POS*0.1)) ) offset[2]--;
        if( (angulo[2]<(MAX_POS*0.1)) && (angulo_1[2]>(MAX_POS*0.9)) ) offset[2]++;

        angulo_real_1[2] = angulo_real[2];
        angulo_real[2] = angulo[2] + offset[2]*MAX_POS;
        PWMvalue[2] = calcularPIDFF(2, qds[2], dqds[2], d2qds[2], angulo_real[2]);
        setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
      }
    }
    // Control individual de cada motor
    // Motor Delta 1
    if(flag_control_M1){
      PCA9548A_cambio_direccion(0,1);
      angulo_1[0]= angulo[0];
      angulo[0] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      else{
        if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
        if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;

        angulo_real_1[0] = angulo_real[0];
        angulo_real[0] = angulo[0] + offset[0]*MAX_POS;
        PWMvalue[0] = calcularPID(0, qds[0], angulo_real[0]);
        setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      }
    }
    // Motor Delta 2
    if(flag_control_M2){
      PCA9548A_cambio_direccion(1,1);
      angulo_1[1]= angulo[1];
      angulo[1] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
      else{
        if( (angulo[1]>(MAX_POS*0.9)) && (angulo_1[1]<(MAX_POS*0.1)) ) offset[1]--;
        if( (angulo[1]<(MAX_POS*0.1)) && (angulo_1[1]>(MAX_POS*0.9)) ) offset[1]++;

        angulo_real_1[1] = angulo_real[1];
        angulo_real[1] = angulo[1] + offset[1]*MAX_POS;
        PWMvalue[1] = calcularPID(1, qds[1], angulo_real[1]);
        setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
      }
    }
    // Motor Delta 3
    if(flag_control_M3){
      PCA9548A_cambio_direccion(2,1);
      angulo_1[2]= angulo[2];
      angulo[2] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
      else{
        if( (angulo[2]>(MAX_POS*0.9)) && (angulo_1[2]<(MAX_POS*0.1)) ) offset[2]--;
        if( (angulo[2]<(MAX_POS*0.1)) && (angulo_1[2]>(MAX_POS*0.9)) ) offset[2]++;

        angulo_real_1[2] = angulo_real[2];
        angulo_real[2] = angulo[2] + offset[2]*MAX_POS;
        PWMvalue[2] = calcularPIDFF(2, qds[2], dqds[2], d2qds[2], angulo_real[2]);
        setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
      }
    }
    // Motor Manipulador
    if(flag_control_M4){
      PCA9548A_cambio_direccion(3,1);
      angulo_1[3]= angulo[3];
      angulo[3] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
      else{
        if( (angulo[3]>(MAX_POS*0.9)) && (angulo_1[3]<(MAX_POS*0.1)) ) offset[3]--;
        if( (angulo[3]<(MAX_POS*0.1)) && (angulo_1[3]>(MAX_POS*0.9)) ) offset[3]++;

        angulo_real_1[3] = angulo_real[3];
        angulo_real[3] = angulo[3] + offset[3]*MAX_POS;
        PWMvalue[3] = calcularPID(3, qds[3], angulo_real[3]);
        setMotor(PWMvalue[3], PWMChannelIN1_3, PWMChannelIN2_3);
        if(error[3] < error_min){
          setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
          flag_control_M4 = false;
        }
      }
    }
    // Motor Cambio de Herramienta
    if(flag_control_M5){
      PCA9548A_cambio_direccion(4,1);
      angulo_1[4]= angulo[4];
      angulo[4] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
      else{
        if( (angulo[4]>(MAX_POS*0.9)) && (angulo_1[4]<(MAX_POS*0.1)) ) offset[4]--;
        if( (angulo[4]<(MAX_POS*0.1)) && (angulo_1[4]>(MAX_POS*0.9)) ) offset[4]++;

        angulo_real_1[4] = angulo_real[4];
        angulo_real[4] = angulo[4] + offset[4]*MAX_POS;
        PWMvalue[4] = calcularPID(4, qds[4], angulo_real[4]);
        setMotor(PWMvalue[4], PWMChannelIN1_4, PWMChannelIN2_4);

        if(error[4] < error_min){
          setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
          flag_control_M5 = false;
        }
      }
    }
    // Motor Inventario
    if(flag_control_M6){
      PCA9548A_cambio_direccion(5,1);
      angulo_1[5]= angulo[5];
      angulo[5] = leerMT6701();
      if( i2c_not_present ) setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
      else{
        if( (angulo[5]>(MAX_POS*0.9)) && (angulo_1[5]<(MAX_POS*0.1)) ) offset[5]--;
        if( (angulo[5]<(MAX_POS*0.1)) && (angulo_1[5]>(MAX_POS*0.9)) ) offset[5]++;

        angulo_real_1[5] = angulo_real[5];
        angulo_real[5] = angulo[5] + offset[5]*MAX_POS;
        PWMvalue[5] = calcularPID(5, qds[5], angulo_real[5]);
        setMotor(PWMvalue[5], PWMChannelIN1_5, PWMChannelIN2_5);

        if(error[5] < error_min){
          setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
          flag_control_M6 = false;
        }
      }
    }
    // Muestra los valores para monitorear el comportamiento del PID
    if(flag_mostrar_valores_PID){      
      // Serial.print("PosRef:"); Serial.print(qds[0],5); Serial.print(",");
      Serial.print("PosRef:"); Serial.print(qds[0],5); Serial.print(",");
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

  // Serial.print("Comando: "), Serial.print(comm1), Serial.print(" "), Serial.println(comm2);
  // Serial.print("Arg1: "), Serial.println(args[0]);
  // Serial.print("Arg2: "), Serial.println(args[1]);
  // Serial.print("Arg3: "), Serial.println(args[2]);
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
          flag_control_M123 = true;
          flag_control_M1 = false;
          flag_control_M2 = false;
          flag_control_M3 = false;
          qds[0] = args[0];
          dqds[0] = args[1];
          d2qds[0] = args[2];
          qds[1] = args[3];
          dqds[1] = args[4];
          d2qds[1] = args[5];
          qds[2] = args[6];
          dqds[2] = args[7];
          d2qds[2] = args[8];
          break;
        case 1:
          flag_control_M123 = false;
          flag_control_M1 = true;
          qds[0] = args[0];
          dqds[0] = 0.0;
          d2qds[0] = 0.0;
          break;
        case 2:
          flag_control_M123 = false;
          flag_control_M2 = true;
          qds[1] = args[0];
          dqds[1] = 0.0;
          d2qds[1] = 0.0;
          break;
        case 3:
          flag_control_M123 = false;
          flag_control_M3 = true;
          qds[2] = args[0];
          dqds[2] = 0.0;
          d2qds[2] = 0.0;
          break;
        case 4:
          flag_control_M4 = true;
          qds[3] = args[0];
          break;
        case 5:
          // if(flag_HOME_realizado){
            qds[4] = args[0];
            if((qds[4] < max_pos_herr) & (qds[4] > min_pos_herr)) flag_control_M5 = true;
            else Serial.println("Posicion excede los limites de herramienta");
          // }
          break;
        case 6:
          flag_control_M6 = true;
          qds[5] = args[0];
          break;
        default:
          Serial.println("No existe ese motor");
          break;
      }
      break;
    // Mueve el motor seleccionado a una velocidad durante un tiempo
    case 'U':
      switch(comm2.toInt()) {
        case 1:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_0, PWMChannelIN2_0); // Amplitud en % y periodo en us
          break;
        case 2:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_1, PWMChannelIN2_1); // Amplitud en % y periodo en us
          break;
        case 3:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_2, PWMChannelIN2_2); // Amplitud en % y periodo en us
          break;
        case 4:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_3, PWMChannelIN2_3); // Amplitud en % y periodo en us
          break;
        case 5:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_4, PWMChannelIN2_4); // Amplitud en % y periodo en us
          break;
        case 6:
          amplitud = args[0];
          periodo = args[1];
          gen_pulso(amplitud, periodo, PWMChannelIN1_5, PWMChannelIN2_5); // Amplitud en % y periodo en us
          break;
        default:
          Serial.println("No existe ese motor");
          break;
      }
      break;
    // Mandar un pulso para dispensar soldadura
    case 'S':
      amplitud = args[0];
      periodo = args[1];
      gen_pulso(amplitud, periodo, PWMChannelIN1_6, PWMChannelIN2_6); // Amplitud en % y periodo en us
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
      HOME();
      break;
    case 'T':
      switch(comm2.toInt()) {
        case 0: // herramienta camara
          flag_control_M4 = true;
          qds[3] = pos_herramienta_0; 
          break;
        case 1: // dispensador de soldadura
          flag_control_M4 = true;
          qds[3] = pos_herramienta_1;
          break;
        case 2: // manipulador
          flag_control_M4 = true;
          qds[3] = pos_herramienta_2;
          break;
        default:
          Serial.println("No existe esa herramienta");
          break;
      }
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
    case 'C':
      pos_herramienta_0 = args[0];
      break;
    case 'D':
      pos_herramienta_1 = args[0];
      break;
    case 'P':
      pos_herramienta_2 = args[0];
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
  i2c_not_present = Wire.endTransmission();

  if(i2c_not_present == 0){
    Wire.requestFrom(_address, 1);
    if (Wire.available() >= 1) {
      single_byte = Wire.read();
      i2c_not_present = false;
    }
    Wire.endTransmission();
  }

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
  // errorD[motor] = (error[motor]-error_1[motor])/(sampleTime*0.001); // Error derivativo
  error_1[motor] = error[motor]; // Error anterior
  
  return Kp[motor]*error[motor]+Ki[motor]*errorI[motor]+Kd[motor]*(error[motor]-error_1[motor])/(sampleTime*0.001);
}

// Calcular PID
// float calcularPID2(int motor, float setpoint, float input){
//   z_2[motor] = z_1[motor];
//   z_1[motor] = z[motor];
//   z[motor] = setpoint - input;
//   error[motor] = z[motor];

//   u_1[motor] = u[motor];
//   u[motor] = K1*z[motor] + K2*z_1[motor] + K3*z_2[motor] + u_1[motor];
//   return u[motor];
// }

// Calcular PID con prealimentacion (feed-forward)
float calcularPIDFF(int motor, float qd, float dqd, float d2qd, float q){
  // qd   : pos deseada (trayectoria)
  // dqd  : vel deseada (trayectoria)
  // d2qd : acel deseada (trayectoria)
  // q    : pos real (medida)
  error[motor] = q-qd; // Error actual
  errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
  error_1[motor] = error[motor]; // Error anterior
  return J*d2qd + B*dqd - J*( Kp[motor]*error[motor] + Ki[motor]*errorI[motor] + Kd[motor]*(error[motor] - error_1[motor])/(sampleTime*0.001) );
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

// Homing para la herramienta
void HOME(){
  bool switch_herramienta = false; // Se declara variable para leer el limit switch
  setMotor(vel_alta, PWMChannelIN1_4, PWMChannelIN2_4); // Se inicializa el motor en velocidad alta en direccion al limit switch (verificar direccion si no cambiar todas las vels por -1)
  while(switch_herramienta == false) switch_herramienta = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4); // Detener el motor
  delay(100);
  setMotor(-vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido contrario dos segundos
  delay(2000);
  setMotor(vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido al limit switch en velocidad baja
  while(switch_herramienta == false) switch_herramienta = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4); // Detener el motor
  PCA9548A_cambio_direccion(4,1); // Dirigir el multiplexor I2C al encoder 5
  pos_home_herr = leerMT6701(); // Guardar la lectura del encoder
  flag_HOME_realizado = true;
}

// Generador de pulso 
void gen_pulso(float amp, float ancho, int IN1, int IN2){ // Amplitud en % y periodo en us
  setMotor(amp, IN1, IN2);
  delayMicroseconds(ancho);
  setMotor(0.0, IN1, IN2);
}