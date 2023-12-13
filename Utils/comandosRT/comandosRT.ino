/*                              Elaboro: Saul Asis Cuevas Morales
                                      Luis Fernando Morales Flores 

                                         PINOUT ESP32 38 PINES
                                          _________________
                            X      3.3V  |                 |GND        X
                                   EN    |                 |GPIO23     X
                            O      GPIO36|                 |GPIO22 SCL X
                            O      GPIO39|                 |GPIO1      -
                            O      GPIO34|                 |GPIO3      O
                            O      GPIO35|                 |GPIO21 SDA X
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
bool i2c_not_present[7] = {true, true, true, true, true, true, true};

// Tiempo de muestreo
unsigned long lastTime = 0; // Tiempo anterior
unsigned long loopTime = 0; // Tiempo anterior Loop de Lectura
unsigned long loopTime2 = 0; // Tiempo anterior Loop de Lectura
unsigned long loopTime3 = 0; // Tiempo anterior Loop de Lectura
unsigned long lastTime3 = 0;
unsigned long lastTime2 = 0;
unsigned long sampleTime = 10; // Tiempo de muestreo en milisegundos

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
// const float B = 3.310322593720104; // Constante de amortiguamiento
// const float J = 0.085702607785979; // Constante de inercia
float B = 5.0; // Constante de amortiguamiento
float J = 5.0; // Constante de inercia

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
const float zeros[3] = {2.95138, 0.67725, 1.18078};
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
const float vel_alta = 20.0;
const float vel_baja = 10.0;
const float max_pos_herr = 100.0;
const float min_pos_herr = -100.0;
float pos_herramienta_0 = -5.85;
float pos_herramienta_1 = -11.7;
float pos_herramienta_2 = 0.0;
bool hit_limit = false;

// Parametros del PID
const float error_min = 0.006;

const float Kp[6] = {1412.13, 1412.13, 1412.13, 553.0961, 865.5567, 865.5567};
const float Ki[6] = {0.0, 0.0, 0.0, 2258.7612, 0.0, 0.0};
const float Kd[6] = {68.2507, 68.2507, 68.2507, 1.4123, 57.3356, 57.3356};

// Variables del PID
float error[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float error_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorI[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorD[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

TaskHandle_t Lectura;

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

  // Wire.setClock(400000);
  Wire.setTimeout(1);
  Wire.begin(-1, -1, 400000);

  PCA9548A_cambio_direccion(0,1);
  angulo_real[0] = leerMT6701(0) - zeros[0];
  PCA9548A_cambio_direccion(1,1);
  angulo_real[1] = leerMT6701(1) - zeros[1];
  PCA9548A_cambio_direccion(2,1);
  angulo_real[2] = leerMT6701(2) - zeros[2];
  PCA9548A_cambio_direccion(3,1);
  angulo_real[3] = leerMT6701(3) - zeros[3];
  PCA9548A_cambio_direccion(4,1);
  angulo_real[4] = leerMT6701(4) - zeros[4];
  PCA9548A_cambio_direccion(5,1);
  angulo_real[5] = leerMT6701(5) - zeros[5];

  Serial.begin(250000);     

  xTaskCreatePinnedToCore(
                    LecturaLoop,   /* Task function. */
                    "Lectura",     /* name of task. */
                    10000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    tskIDLE_PRIORITY,           /* priority of the task */
                    &Lectura,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */
}

// Se encarga de leer el puerto serial y comunicacion I2C
void LecturaLoop( void * pvParameters ){
  for(;;){
    lastTime2 = millis();
    if (strComplete) {
      descifrar_comando();
      str = "";
      strComplete = false;
    }

    hit_limit = digitalRead(pinLIMIT_SW);

    PCA9548A_cambio_direccion(0,1);
    // angulo_1[0]= angulo[0];
    // angulo[0] = leerMT6701(0);
    // if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
    // if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;
    // angulo_real_1[0] = angulo_real[0];
    // angulo_real[0] = angulo[0] + offset[0]*MAX_POS - zeros[0];

    // PCA9548A_cambio_direccion(1,1);
    // angulo_1[1]= angulo[1];
    // angulo[1] = leerMT6701(1);
    // if( (angulo[1]>(MAX_POS*0.9)) && (angulo_1[1]<(MAX_POS*0.1)) ) offset[1]--;
    // if( (angulo[1]<(MAX_POS*0.1)) && (angulo_1[1]>(MAX_POS*0.9)) ) offset[1]++;
    // angulo_real_1[1] = angulo_real[1];
    // angulo_real[1] = angulo[1] + offset[1]*MAX_POS - zeros[1];

    // PCA9548A_cambio_direccion(2,1);
    // angulo_1[2]= angulo[2];
    // angulo[2] = leerMT6701(2);
    // if( (angulo[2]>(MAX_POS*0.9)) && (angulo_1[2]<(MAX_POS*0.1)) ) offset[2]--;
    // if( (angulo[2]<(MAX_POS*0.1)) && (angulo_1[2]>(MAX_POS*0.9)) ) offset[2]++;
    // angulo_real_1[2] = angulo_real[2];
    // angulo_real[2] = angulo[2] + offset[2]*MAX_POS - zeros[2];

    // PCA9548A_cambio_direccion(3,1);
    // angulo_1[3]= angulo[3];
    // angulo[3] = leerMT6701(3);
    // if( (angulo[3]>(MAX_POS*0.9)) && (angulo_1[3]<(MAX_POS*0.1)) ) offset[3]--;
    // if( (angulo[3]<(MAX_POS*0.1)) && (angulo_1[3]>(MAX_POS*0.9)) ) offset[3]++;
    // angulo_real_1[3] = angulo_real[3];
    // angulo_real[3] = angulo[3] + offset[3]*MAX_POS - zeros[3];

    // PCA9548A_cambio_direccion(4,1);
    // angulo_1[4]= angulo[4];
    // angulo[4] = leerMT6701(4);
    // if( (angulo[4]>(MAX_POS*0.9)) && (angulo_1[4]<(MAX_POS*0.1)) ) offset[4]--;
    // if( (angulo[4]<(MAX_POS*0.1)) && (angulo_1[4]>(MAX_POS*0.9)) ) offset[4]++;
    // angulo_real_1[4] = angulo_real[4];
    // angulo_real[4] = angulo[4] + offset[4]*MAX_POS - zeros[4];

    // PCA9548A_cambio_direccion(5,1);
    // angulo_1[5]= angulo[5];
    // angulo[5] = leerMT6701(5);
    // if( (angulo[5]>(MAX_POS*0.9)) && (angulo_1[5]<(MAX_POS*0.1)) ) offset[5]--;
    // if( (angulo[5]<(MAX_POS*0.1)) && (angulo_1[5]>(MAX_POS*0.9)) ) offset[5]++;
    // angulo_real_1[5] = angulo_real[5];
    // angulo_real[5] = angulo[5] + offset[5]*MAX_POS - zeros[5];

    // // Lectura en conjunto de los motores delta
    // if(flag_control_M123){
    //   PCA9548A_cambio_direccion(0,1);
    //   angulo_1[0]= angulo[0];
    //   angulo[0] = leerMT6701(0);
    //   if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
    //   if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;
    //   angulo_real_1[0] = angulo_real[0];
    //   angulo_real[0] = angulo[0] + offset[0]*MAX_POS - zeros[0];

    //   PCA9548A_cambio_direccion(1,1);
    //   angulo_1[1]= angulo[1];
    //   angulo[1] = leerMT6701(1);
    //   if( (angulo[1]>(MAX_POS*0.9)) && (angulo_1[1]<(MAX_POS*0.1)) ) offset[1]--;
    //   if( (angulo[1]<(MAX_POS*0.1)) && (angulo_1[1]>(MAX_POS*0.9)) ) offset[1]++;
    //   angulo_real_1[1] = angulo_real[1];
    //   angulo_real[1] = angulo[1] + offset[1]*MAX_POS - zeros[1];

    //   PCA9548A_cambio_direccion(2,1);
    //   angulo_1[2]= angulo[2];
    //   angulo[2] = leerMT6701(2);
    //   if( (angulo[2]>(MAX_POS*0.9)) && (angulo_1[2]<(MAX_POS*0.1)) ) offset[2]--;
    //   if( (angulo[2]<(MAX_POS*0.1)) && (angulo_1[2]>(MAX_POS*0.9)) ) offset[2]++;
    //   angulo_real_1[2] = angulo_real[2];
    //   angulo_real[2] = angulo[2] + offset[2]*MAX_POS - zeros[2];
    // }
    // // Lectura individual de cada motor
    // // Motor Delta 1
    // if(flag_control_M1){
    //   PCA9548A_cambio_direccion(0,1);
    //   angulo_1[0]= angulo[0];
    //   angulo[0] = leerMT6701(0) - zeros[0];
    //   if( (angulo[0]>(MAX_POS*0.9)) && (angulo_1[0]<(MAX_POS*0.1)) ) offset[0]--;
    //   if( (angulo[0]<(MAX_POS*0.1)) && (angulo_1[0]>(MAX_POS*0.9)) ) offset[0]++;
    //   angulo_real_1[0] = angulo_real[0];
    //   angulo_real[0] = angulo[0] + offset[0]*MAX_POS - zeros[0];
    // }
    // // Motor Delta 2
    // if(flag_control_M2){
    //   PCA9548A_cambio_direccion(1,1);
    //   angulo_1[1]= angulo[1];
    //   angulo[1] = leerMT6701(1);
    //   if( (angulo[1]>(MAX_POS*0.9)) && (angulo_1[1]<(MAX_POS*0.1)) ) offset[1]--;
    //   if( (angulo[1]<(MAX_POS*0.1)) && (angulo_1[1]>(MAX_POS*0.9)) ) offset[1]++;
    //   angulo_real_1[1] = angulo_real[1];
    //   angulo_real[1] = angulo[1] + offset[1]*MAX_POS - zeros[1];
    // }
    // // Motor Delta 3
    // if(flag_control_M3){
    //   PCA9548A_cambio_direccion(2,1);
    //   angulo_1[2]= angulo[2];
    //   angulo[2] = leerMT6701(2);
    //   if( (angulo[2]>(MAX_POS*0.9)) && (angulo_1[2]<(MAX_POS*0.1)) ) offset[2]--;
    //   if( (angulo[2]<(MAX_POS*0.1)) && (angulo_1[2]>(MAX_POS*0.9)) ) offset[2]++;
    //   angulo_real_1[2] = angulo_real[2];
    //   angulo_real[2] = angulo[2] + offset[2]*MAX_POS - zeros[2];
    // }
    // // Motor Manipulador
    // if(flag_control_M4){
    //   PCA9548A_cambio_direccion(3,1);
    //   angulo_1[3]= angulo[3];
    //   angulo[3] = leerMT6701(3);
    //   if( (angulo[3]>(MAX_POS*0.9)) && (angulo_1[3]<(MAX_POS*0.1)) ) offset[3]--;
    //   if( (angulo[3]<(MAX_POS*0.1)) && (angulo_1[3]>(MAX_POS*0.9)) ) offset[3]++;
    //   angulo_real_1[3] = angulo_real[3];
    //   angulo_real[3] = angulo[3] + offset[3]*MAX_POS - zeros[3];
    // }
    // // Motor Cambio de Herramienta
    // if(flag_control_M5){
    //   PCA9548A_cambio_direccion(4,1);
    //   angulo_1[4]= angulo[4];
    //   angulo[4] = leerMT6701(4);
    //   if( (angulo[4]>(MAX_POS*0.9)) && (angulo_1[4]<(MAX_POS*0.1)) ) offset[4]--;
    //   if( (angulo[4]<(MAX_POS*0.1)) && (angulo_1[4]>(MAX_POS*0.9)) ) offset[4]++;
    //   angulo_real_1[4] = angulo_real[4];
    //   angulo_real[4] = angulo[4] + offset[4]*MAX_POS - zeros[4];
    // }
    // // Motor Inventario
    // if(flag_control_M6){
    //   PCA9548A_cambio_direccion(5,1);
    //   angulo_1[5]= angulo[5];
    //   angulo[5] = leerMT6701(5);
    //   if( (angulo[5]>(MAX_POS*0.9)) && (angulo_1[5]<(MAX_POS*0.1)) ) offset[5]--;
    //   if( (angulo[5]<(MAX_POS*0.1)) && (angulo_1[5]>(MAX_POS*0.9)) ) offset[5]++;
    //   angulo_real_1[5] = angulo_real[5];
    //   angulo_real[5] = angulo[5] + offset[5]*MAX_POS - zeros[5];
    // }

    if(millis() - loopTime >= sampleTime){
      // Muestra los valores para monitorear el comportamiento del PID
      if(flag_mostrar_valores_PID){   
        int motorprint = 0;
        // Serial.print("PosRef:"); Serial.print(qds[0],5); Serial.print(",");
        Serial.print("PosRef:"); Serial.print(qds[motorprint],5); Serial.print(",");
        Serial.print("Pos:"); Serial.print(angulo_real[motorprint],5); Serial.print(",");
        Serial.print("Error:"); Serial.print(error[motorprint],5); Serial.print(",");
        Serial.print("PID:"); Serial.println(PWMvalue[motorprint],5);
      }
      loopTime = millis();
    }
    loopTime2 = millis() - lastTime2;
  }
}

void loop() {
  lastTime3 = millis();
  if(millis() - lastTime >= sampleTime){
    // Control en conjunto de los motores delta
    if(flag_control_M123){
      if( i2c_not_present[0] ) setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      else{
        PWMvalue[0] = calcularPIDFF(0, qds[0], dqds[0], d2qds[0], angulo_real[0])*-1;
        setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      }

      if( i2c_not_present[1] ) setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
      else{
        PWMvalue[1] = calcularPIDFF(1, qds[1], dqds[1], d2qds[1], angulo_real[1])*-1;
        setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
      }

      if( i2c_not_present[2] ) setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
      else{
        PWMvalue[2] = calcularPIDFF(2, qds[2], dqds[2], d2qds[2], angulo_real[2])*-1;
        setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
      }
    }
    // Control individual de cada motor
    // Motor Delta 1
    if(flag_control_M1){
      if( i2c_not_present[0] ) setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
      else{
        PWMvalue[0] = calcularPID(0, qds[0], angulo_real[0])*-1;
        setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
      }
    }
    // Motor Delta 2
    if(flag_control_M2){
      if( i2c_not_present[1] ) setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
      else{
        PWMvalue[1] = calcularPID(1, qds[1], angulo_real[1])*-1;
        setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
      }
    }
    // Motor Delta 3
    if(flag_control_M3){
      if( i2c_not_present[2] ) setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
      else{
        PWMvalue[2] = calcularPID(2, qds[2], angulo_real[2])*-1;
        setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
      }
    }
    // Motor Manipulador
    if(flag_control_M4){
      if( i2c_not_present[3] ) setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
      else{
        PWMvalue[3] = calcularPID(3, qds[3], angulo_real[3]);
        setMotor(PWMvalue[3], PWMChannelIN1_3, PWMChannelIN2_3);
      }
    }
    // Motor Cambio de Herramienta
    if(flag_control_M5){
      if( i2c_not_present[4] ) setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
      else{
        PWMvalue[4] = calcularPID(4, qds[4], angulo_real[4]);
        if( hit_limit == false & PWMvalue[4] > 0) {
          setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
          flag_control_M5 = false;
        }
        else setMotor(PWMvalue[4], PWMChannelIN1_4, PWMChannelIN2_4);
        if(abs(error[4]) < error_min){
          setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
          flag_control_M5 = false;
        }
      }
    }
    // Motor Inventario
    if(flag_control_M6){
      if( i2c_not_present[5] ) setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
      else{
        PWMvalue[5] = calcularPID(5, qds[5], angulo_real[5]);
        setMotor(PWMvalue[5], PWMChannelIN1_5, PWMChannelIN2_5);
        if(abs(error[5]) < error_min){
          setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
          flag_control_M6 = false;
        }
      }
    }
    lastTime = millis();
  }
  loopTime3 = millis() - lastTime3;
  Serial.print(loopTime2); Serial.print(", "); Serial.println(loopTime3);
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
          if( hit_limit == false & amplitud > 0) ;
          else gen_pulso(amplitud, periodo, PWMChannelIN1_4, PWMChannelIN2_4); // Amplitud en % y periodo en us
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
      // Serial.println("Quieres leer los encoders");
      PCA9548A_cambio_direccion(0, 1);
      angulo_real[0] = leerMT6701(0) - zeros[0];
      Serial.print(angulo_real[0]), Serial.print(" ");
      PCA9548A_cambio_direccion(1, 1);
      angulo_real[1] = leerMT6701(1) - zeros[1];
      Serial.print(angulo_real[1]), Serial.print(" ");
      PCA9548A_cambio_direccion(2, 1);
      angulo_real[2] = leerMT6701(2) - zeros[2];
      Serial.print(angulo_real[2]), Serial.print(" ");
      PCA9548A_cambio_direccion(3, 1);
      angulo_real[3] = leerMT6701(3) - zeros[3];
      Serial.print(angulo_real[3]), Serial.print(" ");
      PCA9548A_cambio_direccion(4, 1);
      angulo_real[4] = leerMT6701(4) - zeros[4];
      Serial.print(angulo_real[4]), Serial.print(" ");
      PCA9548A_cambio_direccion(5, 1);
      angulo_real[5] = leerMT6701(5) - zeros[5];
      Serial.println(angulo_real[5]);
      PCA9548A_cambio_direccion(0, 0); // reset
      break;
    // HOME a herramienta
    case 'H':
      HOME_BRAZO();
      break;
    case 'T':
      switch(comm2.toInt()) {
        case 0: // herramienta camara
          flag_control_M5 = true;
          qds[4] = pos_home_herr + pos_herramienta_0; 
          Serial.println(qds[4]);
          break;
        case 1: // dispensador de soldadura
          flag_control_M5 = true;
          qds[4] = pos_home_herr + pos_herramienta_1;
          break;
        case 2: // manipulador
          flag_control_M5 = true;
          qds[4] = pos_home_herr + pos_herramienta_2;
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
      if( comm2.toInt() ) {
        flag_mostrar_valores_PID = true;
        PCA9548A_cambio_direccion(0,1);
        angulo_real[0] = leerMT6701(0);
        PCA9548A_cambio_direccion(1,1);
        angulo_real[1] = leerMT6701(1);
        PCA9548A_cambio_direccion(2,1);
        angulo_real[2] = leerMT6701(2);
        PCA9548A_cambio_direccion(3,1);
        angulo_real[3] = leerMT6701(3);
        PCA9548A_cambio_direccion(4,1);
        angulo_real[4] = leerMT6701(4);
        PCA9548A_cambio_direccion(5,1);
        angulo_real[5] = leerMT6701(5);
      }
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
      flag_control_M123 = false;
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

uint8_t I2C_request_single_byte(int _address, int _reg_addr, int motor) {
  uint8_t single_byte = 0;

  Wire.beginTransmission(_address);
  Wire.write(_reg_addr);
  i2c_not_present[motor] = Wire.endTransmission();

  if(i2c_not_present[motor] == 0){
    Wire.requestFrom(_address, 1);
    if (Wire.available() >= 1) {
      single_byte = Wire.read();
      i2c_not_present[motor] = false;
    }
  }

  return single_byte;
}

// Funcion para leer en radianes el encoder magnetico
float leerMT6701(int motor) {
  byte slaveByte1 = I2C_request_single_byte(MT6701_ADDRESS, 0x03, motor);
  byte slaveByte2 = I2C_request_single_byte(MT6701_ADDRESS, 0x04, motor);

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

// Homing para la herramienta
void HOME(){
  bool switch_herramienta = true; // Se declara variable para leer el limit switch
  setMotor(vel_alta, PWMChannelIN1_4, PWMChannelIN2_4); // Se inicializa el motor en velocidad alta en direccion al limit switch (verificar direccion si no cambiar todas las vels por -1)
  switch_herramienta = digitalRead(pinLIMIT_SW);
  while(switch_herramienta == true) switch_herramienta = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4); // Detener el motor
  delay(100);
  setMotor(-vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido contrario dos segundos
  delay(2000);
  setMotor(vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido al limit switch en velocidad baja
  switch_herramienta = digitalRead(pinLIMIT_SW);
  while(switch_herramienta == true) switch_herramienta = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4); // Detener el motor
  PCA9548A_cambio_direccion(4,1); // Dirigir el multiplexor I2C al encoder 5
  pos_home_herr = leerMT6701(4); // Guardar la lectura del encoder
  angulo_real[4] = pos_home_herr;
  offset[4] = 0;
  flag_HOME_realizado = true;
  Serial.println(pos_home_herr, 5);
}

// Homing para la herramienta
void HOME_BRAZO(){
  bool switch_brazo = true; // Se declara variable para leer el limit switch
  setMotor(vel_alta, PWMChannelIN1_2, PWMChannelIN2_2); // Se inicializa el motor en velocidad alta en direccion al limit switch (verificar direccion si no cambiar todas las vels por -1)
  switch_brazo = digitalRead(pinLIMIT_SW);
  while(switch_brazo == true) switch_brazo = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2); // Detener el motor
  delay(100);
  setMotor(-vel_baja, PWMChannelIN1_2, PWMChannelIN2_2); // Girar en sentido contrario dos segundos
  delay(2000);
  setMotor(vel_baja, PWMChannelIN1_2, PWMChannelIN2_2); // Girar en sentido al limit switch en velocidad baja
  switch_brazo = digitalRead(pinLIMIT_SW);
  while(switch_brazo == true) switch_brazo = digitalRead(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
  setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2); // Detener el motor
  PCA9548A_cambio_direccion(2,1); // Dirigir el multiplexor I2C al encoder 5
  pos_home_herr = leerMT6701(2); // Guardar la lectura del encoder
  angulo_real[2] = pos_home_herr;
  offset[2] = 0;
  flag_HOME_realizado = true;
  Serial.println(pos_home_herr, 5);
}

// Generador de pulso 
void gen_pulso(float amp, float ancho, int IN1, int IN2){ // Amplitud en % y periodo en us
  setMotor(amp, IN1, IN2);
  delayMicroseconds(abs(ancho));
  setMotor(0.0, IN1, IN2);
}