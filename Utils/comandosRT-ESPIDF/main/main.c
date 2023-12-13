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

#include <math.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "freertos/task.h"
#include "freertos/timers.h"
#include "driver/ledc.h"
#include "driver/uart.h"
#include "freertos/queue.h"
#include "driver/i2c.h"
#include "esp_timer.h"
#include "rom/ets_sys.h"

// static const char *TAG = "Main";

#define STACK_SIZE_LOOP 1024 * 20

#define UART_NUM UART_NUM_0
#define BUF_SIZE 1024
#define STACK_SIZE_UART 1024 * 10

// Direcciones I2C
#define MT6701_ADDRESS 0x06
#define PCA9548A_ADDRESS 0x70
#define TIMEOUT_MS 1

bool i2c_not_present[7] = {false, false, false, false, false, false, false};

// Tiempo de muestreo
// TimerHandle_t xTimer;      // Timer para el Loop de Control
// const int sampleTime = 1000; // Tiempo de muestreo del Loop de Control en ms
// const int timerId = 1;     // ID del timer

// Tiempo de muestreo
unsigned long lastTime = 0;  // Tiempo anterior
unsigned long loopTime = 0;  // Tiempo anterior Loop de Lectura
unsigned long loopTime2 = 0; // Tiempo anterior Loop de Lectura
unsigned long loopTime3 = 0; // Tiempo anterior Loop de Lectura
unsigned long lastTime3 = 0;
unsigned long lastTime2 = 0;
unsigned long sampleTime = 5; // Tiempo de muestreo en milisegundos

// Pines ESP32
const int pinIN1[7] = {32, 25, 27, 15, 4, 17, 18};
const int pinIN2[7] = {33, 26, 14, 2, 16, 5, 19};
const int pinLIMIT_SW = 13;
const int pin3_VIAS = 23;

// Configuracion lectura de datos serial
const char separator = ' ';
#define dataLength 9 // Ex: M123 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567 1.2345 2.3456 3.4567

// Configuracion PWM ESP32
const int PWMfreq = 1000; // 1 kHz
const int PWMChannelIN1_0 = LEDC_CHANNEL_0;
const int PWMChannelIN2_0 = LEDC_CHANNEL_1;
const int PWMChannelIN1_1 = LEDC_CHANNEL_2;
const int PWMChannelIN2_1 = LEDC_CHANNEL_3;
const int PWMChannelIN1_2 = LEDC_CHANNEL_4;
const int PWMChannelIN2_2 = LEDC_CHANNEL_5;
const int PWMChannelIN1_3 = LEDC_CHANNEL_6;
const int PWMChannelIN2_3 = LEDC_CHANNEL_7;
const int PWMChannelIN1_4 = LEDC_CHANNEL_0; // LOW SPEED
const int PWMChannelIN2_4 = LEDC_CHANNEL_1; // LOW SPEED
const int PWMChannelIN1_5 = LEDC_CHANNEL_2; // LOW SPEED
const int PWMChannelIN2_5 = LEDC_CHANNEL_3; // LOW SPEED
const int PWMChannelIN1_6 = LEDC_CHANNEL_4; // LOW SPEED
const int PWMChannelIN2_6 = LEDC_CHANNEL_5; // LOW SPEED
const int PWMResolution = 16;

const int MAX_DUTY_CYCLE = 65535; // 2^PWMResolution - 1

// Parametros del motor
const float ZONA_MUERTA = 10.0; // Porcentaje PWM en donde se vence la zona muerta
const float MAX_POS = M_TWOPI;
float B = 3.310322593720104; // Constante de amortiguamiento
float J = 0.085702607785979; // Constante de inercia
float lim_neg = -1;
float lim_pos = 1.5;
// float B = 5.0; // Constante de amortiguamiento
// float J = 5.0; // Constante de inercia

// Variables globales
float args[dataLength];
float qds[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float dqds[3] = {0.0, 0.0, 0.0};  // Solo se usa para M1, M2 y M3
float d2qds[3] = {0.0, 0.0, 0.0}; // Solo se usa para M1, M2 y M3
float angulo[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float angulo_real_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
int offset[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float PWMvalue[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
// const float zeros[3] = {1.262850, 0.665748, 2.899991};
const float zeros[3] = {3.433816, 4.421700, 2.899991};
float amplitud = 0.0;
float periodo = 0.0;
bool flag_mostrar_valores_PID = false;
bool flag_HOME_realizado = false;
bool flag_control_M1 = false;
bool flag_control_M2 = false;
bool flag_control_M3 = false;
bool flag_lims = false;
bool flag_control_M4 = false;
bool flag_control_M5 = false;
bool flag_control_M6 = false;
bool flag_control_manual = false;
bool flag_control_manual_M1 = false;
bool busy = false;
bool lastbusy = false;

// Memoria de error
#define errs_num 10
float err_mem_0[errs_num] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float err_mem_1[errs_num] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float err_mem_2[errs_num] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float err_mem_0t = 1.0;
float err_mem_1t = 1.0;
float err_mem_2t = 1.0;

// Homing y herramienta
float pos_home_herr = 0.0;
const float vel_alta = 20.0;
const float vel_baja = 15.0;
const float max_pos_herr = 100.0;
const float min_pos_herr = -100.0;
float pos_herramienta_0 = -5.85;
float pos_herramienta_1 = -11.7;
float pos_herramienta_2 = 0.0;
bool hit_limit = false;

// Parametros del PID
const float error_min = 0.001;

const float Kp[6] = {141.213*3, 141.213*3, 141.213*3, 553.0961, 865.5567, 865.5567};
const float Ki[6] = {0.0, 0.0, 0.0, 2258.7612, 0.0, 0.0};
const float Kd[6] = {6.8251*3, 6.82507*3, 6.82507*3, 1.4123, 57.3356, 57.3356};

// Variables del PID
float error[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float error_1[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorI[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float errorD[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

// esp_err_t set_timer(void);
esp_err_t set_GPIO(void);
esp_err_t set_PWM(void);
esp_err_t create_tasks(void);
static esp_err_t set_i2c(void);
void vTaskControlLoop(void *pvParameters);
void vTaskLecturaLoop(void *pvParameters);
static void uart_task(void *pvParameters);
static void init_uart(void);
static QueueHandle_t uart_queue;
void descifrar_comando(uint8_t *data);
static esp_err_t PCA9548A_cambio_direccion(uint8_t _channel, bool _on_off);
float leerMT6701(uint8_t motor);
float calcularPID(int motor, float setpoint, float input);
float calcularPIDFF(int motor, float qd, float dqd, float d2qd, float q);
void setMotor(float valPWM, int IN1, int IN2);
long map(long x, long in_min, long in_max, long out_min, long out_max);
void gen_pulso(float amp, float ancho, int IN1, int IN2);
void HOME(void);
void HOME_BRAZO(void);

void app_main(void)
{
    ESP_ERROR_CHECK(set_i2c());
    set_GPIO();
    set_PWM();
    // set_timer();
    create_tasks();
    init_uart();
    PCA9548A_cambio_direccion(0, 1);
    printf("i2c scan: \n");
    for (uint8_t i = 1; i < 127; i++)
    {
        int ret;
        i2c_cmd_handle_t cmd = i2c_cmd_link_create();
        i2c_master_start(cmd);
        i2c_master_write_byte(cmd, (i << 1) | I2C_MASTER_WRITE, 1);
        i2c_master_stop(cmd);
        ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, pdMS_TO_TICKS(100));
        i2c_cmd_link_delete(cmd);

        if (ret == ESP_OK)
        {
            printf("Found device at: 0x%2x\n", i);
        }
    }
    while (1)
    {
        lastTime2 = esp_timer_get_time();
        hit_limit = gpio_get_level(pinLIMIT_SW);

        PCA9548A_cambio_direccion(0, 1);
        angulo_1[0] = angulo[0];
        angulo[0] = leerMT6701(0);
        if ((angulo[0] > (MAX_POS * 0.9)) & (angulo_1[0] < (MAX_POS * 0.1)))
            offset[0]--;
        if ((angulo[0] < (MAX_POS * 0.1)) & (angulo_1[0] > (MAX_POS * 0.9)))
            offset[0]++;
        angulo_real_1[0] = angulo_real[0];
        angulo_real[0] = angulo[0] + offset[0] * MAX_POS - zeros[0];

        PCA9548A_cambio_direccion(1, 1);
        angulo_1[1] = angulo[1];
        angulo[1] = leerMT6701(1);
        if ((angulo[1] > (MAX_POS * 0.9)) & (angulo_1[1] < (MAX_POS * 0.1)))
            offset[1]--;
        if ((angulo[1] < (MAX_POS * 0.1)) & (angulo_1[1] > (MAX_POS * 0.9)))
            offset[1]++;
        angulo_real_1[1] = angulo_real[1];
        angulo_real[1] = angulo[1] + offset[1] * MAX_POS - zeros[1];

        PCA9548A_cambio_direccion(2, 1);
        angulo_1[2] = angulo[2];
        angulo[2] = leerMT6701(2);
        if ((angulo[2] > (MAX_POS * 0.9)) & (angulo_1[2] < (MAX_POS * 0.1)))
            offset[2]--;
        if ((angulo[2] < (MAX_POS * 0.1)) & (angulo_1[2] > (MAX_POS * 0.9)))
            offset[2]++;
        angulo_real_1[2] = angulo_real[2];
        angulo_real[2] = angulo[2] + offset[2] * MAX_POS - zeros[2];

        if ((angulo_real[0] > lim_pos) | (angulo_real[1] > lim_pos) | (angulo_real[2] > lim_pos) | (angulo_real[0] < lim_neg) | (angulo_real[1] < lim_neg) | (angulo_real[2] < lim_neg))
        {
            flag_lims = true;
        }
        else
        {
            flag_lims = false;
        }

        PCA9548A_cambio_direccion(3, 1);
        angulo_1[3] = angulo[3];
        // angulo[3] = leerMT6701(3);
        if ((angulo[3] > (MAX_POS * 0.9)) & (angulo_1[3] < (MAX_POS * 0.1)))
            offset[3]--;
        if ((angulo[3] < (MAX_POS * 0.1)) & (angulo_1[3] > (MAX_POS * 0.9)))
            offset[3]++;
        angulo_real_1[3] = angulo_real[3];
        angulo_real[3] = angulo[3] + offset[3] * MAX_POS - zeros[3];

        PCA9548A_cambio_direccion(4, 1);
        angulo_1[4] = angulo[4];
        // angulo[4] = leerMT6701(4);
        if ((angulo[4] > (MAX_POS * 0.9)) & (angulo_1[4] < (MAX_POS * 0.1)))
            offset[4]--;
        if ((angulo[4] < (MAX_POS * 0.1)) & (angulo_1[4] > (MAX_POS * 0.9)))
            offset[4]++;
        angulo_real_1[4] = angulo_real[4];
        angulo_real[4] = angulo[4] + offset[4] * MAX_POS - zeros[4];

        PCA9548A_cambio_direccion(5, 1);
        angulo_1[5] = angulo[5];
        // angulo[5] = leerMT6701(5);
        if ((angulo[5] > (MAX_POS * 0.9)) & (angulo_1[5] < (MAX_POS * 0.1)))
            offset[5]--;
        if ((angulo[5] < (MAX_POS * 0.1)) & (angulo_1[5] > (MAX_POS * 0.9)))
            offset[5]++;
        angulo_real_1[5] = angulo_real[5];
        angulo_real[5] = angulo[5] + offset[5] * MAX_POS - zeros[5];

        loopTime2 = esp_timer_get_time() - lastTime2;
    }
}

void vTaskControlLoop(void *pvParameters)
{
    while (1)
    {
        lastTime3 = esp_timer_get_time();
        if (esp_timer_get_time() - lastTime >= sampleTime)
        {
            lastbusy = busy;
            if (flag_control_M1 | flag_control_M2 | flag_control_M3 | flag_control_M4 | flag_control_M5 | flag_control_M6)
            {
                busy = true;
            }
            else
            {
                busy = false;
            }
            if ((lastbusy == true) & (busy == false))
            {
                printf("ready\n");
            }
            // if (busy == true)
            // {
            //     printf("busy\n");
            // }

            // Control de los motores delta
            if (flag_control_manual_M1) 
            {
                gen_pulso(amplitud, periodo, PWMChannelIN1_0, PWMChannelIN2_0); // Amplitud en % y periodo en us
                busy = false;
            }
            else if (flag_control_M1 & !flag_lims)
            {
                if (i2c_not_present[0])
                    setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
                else
                {
                    // PWMvalue[0] = calcularPIDFF(0, qds[0], dqds[0], d2qds[0], angulo_real[0]) * -1;
                    PWMvalue[0] = calcularPID(0, qds[0], angulo_real[0]) * -1;
                    // printf("%f\n", PWMvalue[0]);
                    err_mem_0[0] = err_mem_0[1];
                    err_mem_0[1] = err_mem_0[2];
                    err_mem_0[2] = err_mem_0[3];
                    err_mem_0[3] = err_mem_0[4];
                    err_mem_0[4] = err_mem_0[5];
                    err_mem_0[5] = err_mem_0[6];
                    err_mem_0[6] = err_mem_0[7];
                    err_mem_0[7] = err_mem_0[8];
                    err_mem_0[8] = err_mem_0[9];
                    err_mem_0[9] = error[0];
                    err_mem_0t = 0;
                    for (size_t i = 0; i < errs_num; i++)
                        err_mem_0t = err_mem_0t + fabsf(err_mem_0[i]);

                    if ((err_mem_0t / errs_num) < error_min)
                    {
                        PWMvalue[0] = 0.0;
                        setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
                        flag_control_M1 = false;
                    }
                    else
                    {
                        setMotor(PWMvalue[0], PWMChannelIN1_0, PWMChannelIN2_0);
                    }
                }
            }
            else
            {
                setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_0);
            }
            // Motor Delta 2
            if (flag_control_M2 & !flag_lims)
            {
                if (i2c_not_present[1])
                    setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
                else
                {
                    // PWMvalue[1] = calcularPIDFF(1, qds[1], dqds[1], d2qds[1], angulo_real[1]) * -1;
                    PWMvalue[1] = calcularPID(1, qds[1], angulo_real[1]) * -1;
                    // printf("%f\n", PWMvalue[1]);
                    err_mem_1[0] = err_mem_1[1];
                    err_mem_1[1] = err_mem_1[2];
                    err_mem_1[2] = err_mem_1[3];
                    err_mem_1[3] = err_mem_1[4];
                    err_mem_1[4] = err_mem_1[5];
                    err_mem_1[5] = err_mem_1[6];
                    err_mem_1[6] = err_mem_1[7];
                    err_mem_1[7] = err_mem_1[8];
                    err_mem_1[8] = err_mem_1[9];
                    err_mem_1[9] = error[1];
                    err_mem_1t = 0;
                    for (size_t i = 0; i < errs_num; i++)
                        err_mem_1t = err_mem_1t + fabsf(err_mem_1[i]);

                    if ((err_mem_1t / errs_num) < error_min)
                    {
                        PWMvalue[1] = 0.0;
                        setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
                        flag_control_M2 = false;
                    }
                    else
                    {
                        setMotor(PWMvalue[1], PWMChannelIN1_1, PWMChannelIN2_1);
                    }
                }
            }
            else if (!flag_control_manual)
            {
                setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);
            }
            // Motor Delta 3
            if (flag_control_M3 & !flag_lims)
            {
                if (i2c_not_present[2])
                    setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
                else
                {
                    // PWMvalue[2] = calcularPIDFF(2, qds[2], dqds[2], d2qds[2], angulo_real[2]) * -1;
                    PWMvalue[2] = calcularPID(2, qds[2], angulo_real[2]) * -1;
                    // printf("%f\n", PWMvalue[2]);
                    err_mem_2[0] = err_mem_2[1];
                    err_mem_2[1] = err_mem_2[2];
                    err_mem_2[2] = err_mem_2[3];
                    err_mem_2[3] = err_mem_2[4];
                    err_mem_2[4] = err_mem_2[5];
                    err_mem_2[5] = err_mem_2[6];
                    err_mem_2[6] = err_mem_2[7];
                    err_mem_2[7] = err_mem_2[8];
                    err_mem_2[8] = err_mem_2[9];
                    err_mem_2[9] = error[2];
                    err_mem_2t = 0;
                    for (size_t i = 0; i < errs_num; i++)
                        err_mem_2t = err_mem_2t + fabsf(err_mem_2[i]);

                    if ((err_mem_2t / errs_num) < error_min)
                    {
                        PWMvalue[2] = 0.0;
                        setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
                        flag_control_M3 = false;
                    }
                    // else if ((err_mem_2[9]==err_mem_2[8]) & (err_mem_2[8]==err_mem_2[7]) & PWMvalue[2]>0)
                    // {
                    //     setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
                    // }
                    else
                    {
                        setMotor(PWMvalue[2], PWMChannelIN1_2, PWMChannelIN2_2);
                    }
                }
            }
            else if (!flag_control_manual)
            {
                setMotor(0.0, PWMChannelIN1_2, PWMChannelIN2_2);
            }
            // Motor Manipulador
            if (flag_control_M4)
            {
                if (i2c_not_present[3])
                    setMotor(0.0, PWMChannelIN1_3, PWMChannelIN2_3);
                else
                {
                    PWMvalue[3] = calcularPID(3, qds[3], angulo_real[3]);
                    setMotor(PWMvalue[3], PWMChannelIN1_3, PWMChannelIN2_3);
                }
            }
            // Motor Cambio de Herramienta
            if (flag_control_M5)
            {
                if (i2c_not_present[4])
                    setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
                else
                {
                    PWMvalue[4] = calcularPID(4, qds[4], angulo_real[4]);
                    if ((hit_limit == false) & (PWMvalue[4] > 0))
                    {
                        setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
                        flag_control_M5 = false;
                    }
                    else
                        setMotor(PWMvalue[4], PWMChannelIN1_4, PWMChannelIN2_4);
                    if (fabsf(error[4]) < error_min)
                    {
                        PWMvalue[4] = 0.0;
                        setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);
                        flag_control_M5 = false;
                    }
                }
            }
            // Motor Inventario
            if (flag_control_M6)
            {
                if (i2c_not_present[5])
                    setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
                else
                {
                    PWMvalue[5] = calcularPID(5, qds[5], angulo_real[5]);
                    setMotor(PWMvalue[5], PWMChannelIN1_5, PWMChannelIN2_5);
                    if (fabsf(error[5]) < error_min)
                    {
                        PWMvalue[5] = 0.0;
                        setMotor(0.0, PWMChannelIN1_5, PWMChannelIN2_5);
                        flag_control_M6 = false;
                    }
                }
            }

            // Muestra los valores para monitorear el comportamiento del PID
            if (flag_mostrar_valores_PID)
            {
                int motorprint = 1;
                printf("PosRef:");
                printf("%f", qds[motorprint]);
                printf(",");
                printf("Pos:");
                printf("%f", angulo_real[motorprint]);
                printf(",");
                printf("Ant:");
                printf("%f", angulo_real_1[motorprint]);
                printf(",");
                printf("Error:");
                printf("%f", error[motorprint]);
                printf(",");
                printf("PID:");
                printf("%f", PWMvalue[motorprint]);
                printf(",");
                printf("LoopL:%lu,LoopC:%lu", loopTime2, loopTime3);
                printf("\n");
            }

            lastTime = esp_timer_get_time();
        }
        // if ((esp_timer_get_time() - lastTime3) < 1000)
        //     ets_delay_us(1000);
        loopTime3 = esp_timer_get_time() - lastTime3;
    }
}

esp_err_t set_GPIO(void)
{
    gpio_reset_pin(pinLIMIT_SW);
    gpio_reset_pin(pin3_VIAS);

    gpio_set_direction(pinLIMIT_SW, GPIO_MODE_INPUT);
    gpio_set_direction(pin3_VIAS, GPIO_MODE_OUTPUT);

    return ESP_OK;
}

esp_err_t set_PWM(void)
{
    ledc_timer_config_t timerconfig = {0};
    timerconfig.speed_mode = LEDC_HIGH_SPEED_MODE;
    timerconfig.duty_resolution = PWMResolution;
    timerconfig.timer_num = LEDC_TIMER_0;
    timerconfig.freq_hz = PWMfreq;

    ledc_timer_config(&timerconfig);

    ledc_channel_config_t channelconfigIN1_0 = {0};
    channelconfigIN1_0.gpio_num = pinIN1[0];
    channelconfigIN1_0.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN1_0.channel = PWMChannelIN1_0;
    channelconfigIN1_0.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_0.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_0.duty = 0;

    ledc_channel_config_t channelconfigIN2_0 = {0};
    channelconfigIN2_0.gpio_num = pinIN2[0];
    channelconfigIN2_0.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN2_0.channel = PWMChannelIN2_0;
    channelconfigIN2_0.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_0.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_0.duty = 0;

    ledc_channel_config_t channelconfigIN1_1 = {0};
    channelconfigIN1_1.gpio_num = pinIN1[1];
    channelconfigIN1_1.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN1_1.channel = PWMChannelIN1_1;
    channelconfigIN1_1.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_1.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_1.duty = 0;

    ledc_channel_config_t channelconfigIN2_1 = {0};
    channelconfigIN2_1.gpio_num = pinIN2[1];
    channelconfigIN2_1.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN2_1.channel = PWMChannelIN2_1;
    channelconfigIN2_1.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_1.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_1.duty = 0;

    ledc_channel_config_t channelconfigIN1_2 = {0};
    channelconfigIN1_2.gpio_num = pinIN1[2];
    channelconfigIN1_2.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN1_2.channel = PWMChannelIN1_2;
    channelconfigIN1_2.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_2.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_2.duty = 0;

    ledc_channel_config_t channelconfigIN2_2 = {0};
    channelconfigIN2_2.gpio_num = pinIN2[2];
    channelconfigIN2_2.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN2_2.channel = PWMChannelIN2_2;
    channelconfigIN2_2.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_2.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_2.duty = 0;

    ledc_channel_config_t channelconfigIN1_3 = {0};
    channelconfigIN1_3.gpio_num = pinIN1[3];
    channelconfigIN1_3.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN1_3.channel = PWMChannelIN1_3;
    channelconfigIN1_3.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_3.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_3.duty = 0;

    ledc_channel_config_t channelconfigIN2_3 = {0};
    channelconfigIN2_3.gpio_num = pinIN2[3];
    channelconfigIN2_3.speed_mode = LEDC_HIGH_SPEED_MODE;
    channelconfigIN2_3.channel = PWMChannelIN2_3;
    channelconfigIN2_3.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_3.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_3.duty = 0;

    ledc_channel_config_t channelconfigIN1_4 = {0};
    channelconfigIN1_4.gpio_num = pinIN1[4];
    channelconfigIN1_4.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN1_4.channel = PWMChannelIN1_4;
    channelconfigIN1_4.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_4.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_4.duty = 0;

    ledc_channel_config_t channelconfigIN2_4 = {0};
    channelconfigIN2_4.gpio_num = pinIN2[4];
    channelconfigIN2_4.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN2_4.channel = PWMChannelIN2_4;
    channelconfigIN2_4.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_4.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_4.duty = 0;

    ledc_channel_config_t channelconfigIN1_5 = {0};
    channelconfigIN1_5.gpio_num = pinIN1[5];
    channelconfigIN1_5.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN1_5.channel = PWMChannelIN1_5;
    channelconfigIN1_5.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_5.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_5.duty = 0;

    ledc_channel_config_t channelconfigIN2_5 = {0};
    channelconfigIN2_5.gpio_num = pinIN2[5];
    channelconfigIN2_5.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN2_5.channel = PWMChannelIN2_5;
    channelconfigIN2_5.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_5.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_5.duty = 0;

    ledc_channel_config_t channelconfigIN1_6 = {0};
    channelconfigIN1_6.gpio_num = pinIN1[6];
    channelconfigIN1_6.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN1_6.channel = PWMChannelIN1_6;
    channelconfigIN1_6.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN1_6.timer_sel = LEDC_TIMER_0;
    channelconfigIN1_6.duty = 0;

    ledc_channel_config_t channelconfigIN2_6 = {0};
    channelconfigIN2_6.gpio_num = pinIN2[6];
    channelconfigIN2_6.speed_mode = LEDC_LOW_SPEED_MODE;
    channelconfigIN2_6.channel = PWMChannelIN2_6;
    channelconfigIN2_6.intr_type = LEDC_INTR_DISABLE;
    channelconfigIN2_6.timer_sel = LEDC_TIMER_0;
    channelconfigIN2_6.duty = 0;

    ledc_channel_config(&channelconfigIN1_0);
    ledc_channel_config(&channelconfigIN2_0);
    ledc_channel_config(&channelconfigIN1_1);
    ledc_channel_config(&channelconfigIN2_1);
    ledc_channel_config(&channelconfigIN1_2);
    ledc_channel_config(&channelconfigIN2_2);
    ledc_channel_config(&channelconfigIN1_3);
    ledc_channel_config(&channelconfigIN2_3);
    ledc_channel_config(&channelconfigIN1_4);
    ledc_channel_config(&channelconfigIN2_4);
    ledc_channel_config(&channelconfigIN1_5);
    ledc_channel_config(&channelconfigIN2_5);
    ledc_channel_config(&channelconfigIN1_6);
    ledc_channel_config(&channelconfigIN2_6);

    return ESP_OK;
}

esp_err_t create_tasks(void)
{
    static uint8_t ucParameterToPass;
    TaskHandle_t xHandle = NULL;
    xTaskCreatePinnedToCore(vTaskControlLoop, "ControlLoop", STACK_SIZE_LOOP, &ucParameterToPass, tskIDLE_PRIORITY, &xHandle, 1);
    // xTaskCreatePinnedToCore(vTaskLecturaLoop, "LecturaLoop", STACK_SIZE_LOOP, &ucParameterToPass, 1, &xHandle, 0);
    return ESP_OK;
}

static esp_err_t set_i2c(void)
{
    i2c_config_t i2c_config = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = 21,
        .scl_io_num = 22,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 400000,
        .clk_flags = 0};
    ESP_ERROR_CHECK(i2c_param_config(I2C_NUM_0, &i2c_config));
    ESP_ERROR_CHECK(i2c_driver_install(I2C_NUM_0, I2C_MODE_MASTER, 0, 0, ESP_INTR_FLAG_LEVEL1));
    return ESP_OK;
}

static void init_uart(void)
{
    uart_config_t uart_config = {.baud_rate = 250000, .data_bits = UART_DATA_8_BITS, .parity = UART_PARITY_DISABLE, .stop_bits = UART_STOP_BITS_1, .flow_ctrl = UART_HW_FLOWCTRL_DISABLE, .source_clk = UART_SCLK_APB};
    uart_param_config(UART_NUM, &uart_config);
    uart_set_pin(UART_NUM, 1, 3, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM, BUF_SIZE, BUF_SIZE, 5, &uart_queue, 0);
    xTaskCreatePinnedToCore(uart_task, "uart_task", STACK_SIZE_UART, NULL, 5, NULL, 1);
}

static void uart_task(void *pvParameters)
{
    uart_event_t event;
    uint8_t *data = (uint8_t *)malloc(BUF_SIZE);
    while (1)
    {
        if (xQueueReceive(uart_queue, &event, portMAX_DELAY))
        {
            bzero(data, BUF_SIZE); // Se borran los datos en data
            switch (event.type)
            {
            case UART_DATA:
                uart_read_bytes(UART_NUM, data, event.size, pdMS_TO_TICKS(100));
                uart_flush(UART_NUM);
                // uart_write_bytes(UART_NUM, (const char *) data, len);
                descifrar_comando(data);
                break;

            default:
                break;
            }
            // ESP_LOGI(TAG, "Data received: %s, Core: %d", data, xPortGetCoreID());
        }
    }
}

void descifrar_comando(uint8_t *data)
{
    data[strcspn((char *)data, "\n")] = 0;   // Se borra la nueva linea de la string
    char *token = strtok((char *)data, " "); // Se extrae el primer valor de la string: COMM1+COMM2 ARG1 ARG2 ARG3 ARG4 ARG5 ARG6 ARG7 ARG8 ARG9
    char comm1 = token[0];
    int comm2 = atoi(token + 1);
    for (size_t i = 0; i < dataLength; i++)
    {
        token = strtok(NULL, " ");
        if (token == NULL)
            break;
        else
            args[i] = atof((const char *)token);
    }

    switch (comm1)
    {
    // Mover un motor a la posicion deseada
    // Ej: M4 120.5
    // Ej: M123 12.3 45.6 78.9
    case 'M':
        // printf("Quieres mover el motor "), printfln(comm2.toInt());
        switch (comm2)
        {
        case 123:
            flag_control_M1 = true;
            flag_control_M2 = true;
            flag_control_M3 = true;
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
            flag_control_M1 = true;
            qds[0] = args[0];
            dqds[0] = 0.0;
            d2qds[0] = 0.0;
            break;
        case 2:
            flag_control_M2 = true;
            qds[1] = args[0];
            dqds[1] = 0.0;
            d2qds[1] = 0.0;
            break;
        case 3:
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
            if ((qds[4] < max_pos_herr) & (qds[4] > min_pos_herr))
                flag_control_M5 = true;
            else
                printf("Posicion excede los limites de herramienta\n");
            // }
            break;
        case 6:
            flag_control_M6 = true;
            qds[5] = args[0];
            break;
        default:
            printf("No existe ese motor\n");
            break;
        }
        break;
    // Mueve el motor seleccionado a una velocidad durante un tiempo
    case 'U':
        busy = true;
        switch (comm2)
        {
        case 1:
            flag_control_manual_M1 = true;
            amplitud = args[0];
            periodo = args[1];
            break;
        case 2:
            flag_control_manual = true;
            amplitud = args[0];
            periodo = args[1];
            gen_pulso(amplitud, periodo, PWMChannelIN1_1, PWMChannelIN2_1); // Amplitud en % y periodo en us
            flag_control_manual = false;
            break;
        case 3:
            flag_control_manual = true;
            amplitud = args[0];
            periodo = args[1];
            gen_pulso(amplitud, periodo, PWMChannelIN1_2, PWMChannelIN2_2); // Amplitud en % y periodo en us
            flag_control_manual = false;
            break;
        case 4:
            flag_control_manual = true;
            amplitud = args[0];
            periodo = args[1];
            gen_pulso(amplitud, periodo, PWMChannelIN1_3, PWMChannelIN2_3); // Amplitud en % y periodo en us
            flag_control_manual = false;
            break;
        case 5:
            flag_control_manual = true;
            amplitud = args[0];
            periodo = args[1];
            if ((hit_limit == false) & (amplitud > 0))
                ;
            else
            {
                gen_pulso(amplitud, periodo, PWMChannelIN1_4, PWMChannelIN2_4); // Amplitud en % y periodo en us
            }
            flag_control_manual = false;
            break;
        case 6:
            flag_control_manual = true;
            amplitud = args[0];
            periodo = args[1];
            gen_pulso(amplitud, periodo, PWMChannelIN1_5, PWMChannelIN2_5); // Amplitud en % y periodo en us
            flag_control_manual = false;
            break;
        default:
            printf("No existe ese motor\n");
            break;
        }
        break;
    // Mandar un pulso para dispensar soldadura
    case 'S':
        busy = true;
        amplitud = args[0];
        periodo = args[1];
        gen_pulso(amplitud, periodo, PWMChannelIN1_6, PWMChannelIN2_6); // Amplitud en % y periodo en us
        busy = false;
        break;
    // Leer todos los encoders del robot delta
    // Ej: E
    case 'E':
        // printfln("Quieres leer los encoders");
        // PCA9548A_cambio_direccion(0, 1);
        // angulo_real[0] = leerMT6701(0) - zeros[0];
        printf("%f", angulo_real[0]), printf(" ");
        // PCA9548A_cambio_direccion(1, 1);
        // angulo_real[1] = leerMT6701(1) - zeros[1];
        printf("%f", angulo_real[1]), printf(" ");
        // PCA9548A_cambio_direccion(2, 1);
        // angulo_real[2] = leerMT6701(2) - zeros[2];
        printf("%f", angulo_real[2]), printf(" ");
        // PCA9548A_cambio_direccion(3, 1);
        // angulo_real[3] = leerMT6701(3) - zeros[3];
        printf("%f", angulo_real[3]), printf(" ");
        // PCA9548A_cambio_direccion(4, 1);
        // angulo_real[4] = leerMT6701(4) - zeros[4];
        printf("%f", angulo_real[4]), printf(" ");
        // PCA9548A_cambio_direccion(5, 1);
        // angulo_real[5] = leerMT6701(5) - zeros[5];
        printf("%f\n", angulo_real[5]);
        // PCA9548A_cambio_direccion(0, 0); // reset
        break;
    // HOME a herramienta
    case 'H':
        busy = true;
        HOME_BRAZO();
        busy = false;
        break;
    case 'T':
        busy = true;
        switch (comm2)
        {
        case 0: // herramienta camara
            flag_control_M5 = true;
            qds[4] = pos_home_herr + pos_herramienta_0;
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
            printf("No existe esa herramienta\n");
            break;
        }
        busy = false;
        break;
    // Encender o apagar la valvula de tres vias
    case 'V':
        busy = true;
        if (comm2)
            gpio_set_level(pin3_VIAS, true), printf("Valvula encendida\n");
        else
            gpio_set_level(pin3_VIAS, false), printf("Valvula apagada\n");
        busy = false;
        break;
    case 'X':
        if (comm2)
            flag_mostrar_valores_PID = true;
        else
            flag_mostrar_valores_PID = false;
        break;
    // STOP
    case '-':
        busy = true;
        PWMvalue[0] = 0.0;
        PWMvalue[1] = 0.0;
        PWMvalue[2] = 0.0;
        PWMvalue[3] = 0.0;
        PWMvalue[4] = 0.0;
        PWMvalue[5] = 0.0;
        PWMvalue[6] = 0.0;
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
        busy = false;
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
        printf("No reconozco ese comando %c%i\n", comm1, comm2);
        break;
    }
}

// Funcion para multiplexor I2C
static esp_err_t PCA9548A_cambio_direccion(uint8_t _channel, bool _on_off)
{
    uint8_t command = _on_off ? (0x01 << _channel) : 0x00;
    int ret;
    ret = i2c_master_write_to_device(I2C_NUM_0, PCA9548A_ADDRESS, &command, 1, 1);

    return ret;
}

// Funcion para leer en radianes el encoder magnetico
float leerMT6701(uint8_t motor)
{
    uint8_t rx_data[2];
    uint8_t command = 0x03;
    uint16_t concat = 0;
    int ret;
    ret = i2c_master_write_read_device(I2C_NUM_0, MT6701_ADDRESS, &command, 1, rx_data, 2, 1);
    switch (ret)
    {
    case ESP_OK:
        concat = ((rx_data[0] << 6) | (rx_data[1] >> 2));
        i2c_not_present[motor] = false;
        break;
    case ESP_FAIL:
        i2c_not_present[motor] = true;
        printf("ESP_FAIL: Sending command error, slave hasn't ACK the transfer\n");
        break;
    case ESP_ERR_TIMEOUT:
        i2c_not_present[motor] = true;
        printf("ESP_ERR_TIMEOUT: Operation timeout because the bus is busy\n");
        break;
    case ESP_ERR_INVALID_STATE:
        i2c_not_present[motor] = true;
        printf("ESP_ERR_INVALID_STATE: I2C driver not installed or not in master mode\n");
        break;
    case ESP_ERR_INVALID_ARG:
        i2c_not_present[motor] = true;
        printf("ESP_ERR_INVALID_ARG: Parameter error\n");
        break;
    default:
        i2c_not_present[motor] = true;
        printf("ESP_FAIL: Sending command error, slave hasn't ACK the transfer\n");
        break;
    }

    return ((float)concat * MAX_POS) / 16384.0;
}

// Calcular PID
float calcularPID(int motor, float setpoint, float input)
{
    error[motor] = setpoint - input; // Error actual

    errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
    // errorD[motor] = (error[motor]-error_1[motor])/(sampleTime*0.001); // Error derivativo
    error_1[motor] = error[motor]; // Error anterior

    return Kp[motor] * error[motor] + Ki[motor] * errorI[motor] + Kd[motor] * (error[motor] - error_1[motor]) / (sampleTime * 0.001);
}

// Calcular PID con prealimentacion (feed-forward)
float calcularPIDFF(int motor, float qd, float dqd, float d2qd, float q)
{
    // qd   : pos deseada (trayectoria)
    // dqd  : vel deseada (trayectoria)
    // d2qd : acel deseada (trayectoria)
    // q    : pos real (medida)
    error[motor] = q - qd;                              // Error actual
    errorI[motor] += error[motor] * sampleTime * 0.001; // Error acumulado
    error_1[motor] = error[motor];                      // Error anterior
    return J * d2qd + B * dqd - J * (Kp[motor] * error[motor] + Ki[motor] * errorI[motor] + Kd[motor] * (error[motor] - error_1[motor]) / (sampleTime * 0.001));
}

// Configuracion del motor
void setMotor(float valPWM, int IN1, int IN2)
{
    bool dir = true;
    if (valPWM == 0.0)
    {
        ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN1, 0);
        ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN1);
        ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN2, 0);
        ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN2);
    }
    else
    {
        if (valPWM < 0)
            dir = false;
        valPWM = fabsf(valPWM);
        if (valPWM > 100)
            valPWM = 100;
        if (valPWM < ZONA_MUERTA)
            valPWM = ZONA_MUERTA;
        int dutyCycle = map(valPWM, 0, 100, 0, MAX_DUTY_CYCLE);
        // dir : true = ccw, false = cw
        if (dir)
        {
            ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN1, dutyCycle);
            ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN1);
            ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN2, 0);
            ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN2);
        }
        else
        {
            ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN1, 0);
            ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN1);
            ledc_set_duty(LEDC_HIGH_SPEED_MODE, IN2, dutyCycle);
            ledc_update_duty(LEDC_HIGH_SPEED_MODE, IN2);
        }
    }
}

// Homing para la herramienta
void HOME(void)
{
    bool switch_herramienta = true;                       // Se declara variable para leer el limit switch
    setMotor(vel_alta, PWMChannelIN1_4, PWMChannelIN2_4); // Se inicializa el motor en velocidad alta en direccion al limit switch (verificar direccion si no cambiar todas las vels por -1)
    switch_herramienta = gpio_get_level(pinLIMIT_SW);
    while (switch_herramienta == true)
        switch_herramienta = gpio_get_level(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
    setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);      // Detener el motor
    vTaskDelay(pdMS_TO_TICKS(100));
    setMotor(-vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido contrario dos segundos
    vTaskDelay(pdMS_TO_TICKS(1000));
    setMotor(vel_baja, PWMChannelIN1_4, PWMChannelIN2_4); // Girar en sentido al limit switch en velocidad baja
    switch_herramienta = gpio_get_level(pinLIMIT_SW);
    while (switch_herramienta == true)
        switch_herramienta = gpio_get_level(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
    setMotor(0.0, PWMChannelIN1_4, PWMChannelIN2_4);      // Detener el motor
    PCA9548A_cambio_direccion(4, 1);                      // Dirigir el multiplexor I2C al encoder 5
    pos_home_herr = leerMT6701(4);                        // Guardar la lectura del encoder
    angulo_real[4] = pos_home_herr;
    offset[4] = 0;
    flag_HOME_realizado = true;
    printf("%f\n", pos_home_herr);
}

// Homing para la herramienta
void HOME_BRAZO(void)
{
    bool switch_herramienta = true;                       // Se declara variable para leer el limit switch
    setMotor(vel_alta, PWMChannelIN1_1, PWMChannelIN2_1); // Se inicializa el motor en velocidad alta en direccion al limit switch (verificar direccion si no cambiar todas las vels por -1)
    switch_herramienta = gpio_get_level(pinLIMIT_SW);
    while (switch_herramienta == true)
        switch_herramienta = gpio_get_level(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
    setMotor(0.0, PWMChannelIN1_0, PWMChannelIN2_1);      // Detener el motor
    vTaskDelay(pdMS_TO_TICKS(100));
    setMotor(-vel_baja, PWMChannelIN1_1, PWMChannelIN2_1); // Girar en sentido contrario dos segundos
    vTaskDelay(pdMS_TO_TICKS(2000));
    setMotor(vel_baja, PWMChannelIN1_1, PWMChannelIN2_1); // Girar en sentido al limit switch en velocidad baja
    switch_herramienta = gpio_get_level(pinLIMIT_SW);
    while (switch_herramienta == true)
        switch_herramienta = gpio_get_level(pinLIMIT_SW); // Esperar a leer un positivo (o negativo) en el limit switch
    setMotor(0.0, PWMChannelIN1_1, PWMChannelIN2_1);      // Detener el motor
    // PCA9548A_cambio_direccion(2, 1);                      // Dirigir el multiplexor I2C al encoder 5
    // pos_home_herr = leerMT6701(2);                        // Guardar la lectura del encoder
    // angulo_real[2] = pos_home_herr;
    offset[1] = 0;
    flag_HOME_realizado = true;
    printf("%f\n", angulo_real[1]);
}

// Generador de pulso
void gen_pulso(float amp, float ancho, int IN1, int IN2)
{ // Amplitud en % y periodo en us
    setMotor(amp, IN1, IN2);
    vTaskDelay(pdMS_TO_TICKS(fabsf(ancho) / 1000));
    setMotor(0.0, IN1, IN2);
    flag_control_manual_M1 = false;
}

long map(long x, long in_min, long in_max, long out_min, long out_max)
{
    const long run = in_max - in_min;
    if (run == 0)
    {
        return -1; // AVR returns -1, SAM returns 0
    }
    const long rise = out_max - out_min;
    const long delta = x - in_min;
    return (delta * rise) / run + out_min;
}
