import serial
import time

port = 'COM5'
baudrate = 250000
timeout = 0.001

# herramientas
camara = 0
dispensador = 1
pnp = 2

"""
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
    7 amplitud periodo                                      M7 : Dispensador de soldadura

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

"""

def start_serial():
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    return ser

def stop_serial(ser):
    ser.close()

def read_ESP32(ser):
    data = ser.read_until('\n')
    data = data.strip()
    return data.decode()

def write_ESP32(ser, toSend : bytearray):
    ser.write(toSend+b'\n')

def encender_valvula():
    write_ESP32(b'V1')

def apagar_valvula():
    write_ESP32(b'V0')

def pulso_soldadura(amplitud : float, ancho_pulso : float):
    amplitud = b'%.5f' % amplitud
    ancho_pulso = b'%.5f' % ancho_pulso
    write_ESP32(b'S ' + amplitud + b' ' + ancho_pulso)

def cambio_herramienta(herramienta : int):
    herramienta = b'%i' % herramienta
    write_ESP32(b'H' + herramienta)

def mover_motor(motor : int, pos : float):
    motor = b'%i' % motor
    pos = b'%.5f' % pos
    write_ESP32(b'M' + motor + b' ' + pos)

def desactivar_motores():
    write_ESP32(b'-')

def leer_encoders():
    write_ESP32(b'E')
    return read_ESP32()

def HOME_herramienta():
    write_ESP32(b'H')

def activar_monitoreo():
    write_ESP32(b'X1')

def desactivar_monitoreo():
    write_ESP32(b'X0')

def enviar_trayectoria(ser): # WIP
    f = open('test_trayectorias.txt', 'r')
    lineas = f.readlines()
    cont = 0
    inicio = time.time()
    while True:
        tiempo, comando = lineas[cont].split(' ', 1)
        tiempo = float(tiempo)
        comando = comando.strip().encode('ascii')
        if(time.time()-inicio >= tiempo):
            write_ESP32(ser, comando)
            print(read_ESP32(ser))
            cont += 1
        if(cont > len(lineas)-1):
            break