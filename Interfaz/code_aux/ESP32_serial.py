import serial
import time

# port = 'COM5'
baudrate = 250000
timeout = 0.01

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

def start_serial(port):  
    ser = serial.Serial(port = port, baudrate = baudrate, timeout = timeout)
    #ser.set_buffer_size(rx_size = 12800, tx_size = 12800)
    return ser

def stop_serial(ser):
    ser.close()

def reset(ser):
    ser.reset_input_buffer()

def read_ESP32(ser):
    # data = ser.read_until('\n')
    data = ser.readline()
    data = data.strip(b'\n')
    return data.decode('ascii')

def write_ESP32(ser, toSend : bytearray):
    print(toSend)
    ser.write(toSend+b'\n')

# def write_ESP32(ser, toSend : bytearray):
#     res = toSend.encode()
#     # print(res)
#     ser.write(res)
#     # ser.write()

def encender_valvula(ser):
    write_ESP32(ser, b'V1')

def apagar_valvula(ser):
    write_ESP32(ser, b'V0')

def pulso_soldadura(ser, amplitud : float, ancho_pulso : float):
    am = b'%.5f' % amplitud
    an = b'%.5f' % ancho_pulso
    # text = f"S {amplitud} {ancho_pulso}"
    # write_ESP32(ser, text.encode('ascii'))
    text = b'S' + b' ' + am + b' ' + an
    write_ESP32(ser, text)

def giro_cw(ser, motor : int, amplitud : float, ancho_pulso : float):
    m = b'%i' % motor
    am = b'%.5f' % -amplitud
    an = b'%.5f' % ancho_pulso
    #text = f"U{motor} {amplitud} {ancho_pulso}"
    # write_ESP32(ser, text.encode('ascii'))
    text = b'U' + m + b' ' + am + b' ' + an
    write_ESP32(ser, text)

def giro_ccw(ser, motor : int, amplitud : float, ancho_pulso : float):
    m = b'%i' % motor
    am = b'%.5f' % amplitud
    an = b'%.5f' % ancho_pulso
    # text = f"U{motor} {-amplitud} {ancho_pulso}"
    # write_ESP32(ser, text.encode('ascii'))
    text = b'U' + m + b' ' + am + b' ' + an
    write_ESP32(ser, text)

def cambio_herramienta(ser, herramienta : int):
    herramienta = b'%i' % herramienta
    # text = f"T{herramienta}"
    #write_ESP32(ser, text.encode('ascii'))
    write_ESP32(ser, b'T' + herramienta)

def mover_motor(ser, motor : int, pos : float):
    m = b'%i' % motor
    p = b'%.5f' % pos
    # text = f"M{motor} {pos}"
    # write_ESP32(ser, text.encode('ascii'))
    text = b'M' + m + b' ' + p
    write_ESP32(ser, text)
    
def mover_brazos(ser, pos1 : float, pos2 : float, pos3 : float):
    p1 = b'%.5f' % pos1
    p2 = b'%.5f' % pos2
    p3 = b'%.5f' % pos3
    # text = f"M{motor} {pos}"
    # write_ESP32(ser, text.encode('ascii'))
    text = b'M123' + b' ' + p1 + b' 0 0 ' + p2 + b' 0 0 ' + p3 +  b' 0 0 '
    write_ESP32(ser, text)

def desactivar_motores(ser):
    write_ESP32(ser, b'-')

def leer_encoders(ser):
    write_ESP32(ser, b"E")
    return read_ESP32(ser)

def HOME_herramienta(ser):
    write_ESP32(ser, b'H')

def activar_monitoreo(ser):
    write_ESP32(ser, b'X1')

def desactivar_monitoreo(ser):
    write_ESP32(ser, b'X0')

def reset_ESP(ser):
    write_ESP32(ser, b'R')

def enviar_trayectoria(ser): # WIP
    f = open('temp/archivo_trayectorias.txt', 'r')
    lineas = f.readlines()
    cont = 0
    done = False
    ready = True
    busy = False
    lastTime_ready = time.time()
    inicio = time.time()
    while True:
        rx = read_ESP32(ser)
        rx = str(rx)
        rx = rx[:-1]
        if(len(rx)>0):
            print(rx)
            if(rx[0] == "r"):
                ready = True
                lastTime_ready = time.time()
                print(time.time() - inicio)
                # ser.flush()
        # if(time.time()-lastTime_ready > 5):
        #     done = False
        tiempo, comando = lineas[cont].split(' ', 1)
        tiempo = float(tiempo)
        comando = comando.strip().encode('ascii')
        if(time.time()-inicio >= tiempo):
            if(done == False):
                write_ESP32(ser, comando)
                print(comando.decode())
                done = True
                ready = False
            elif(ready == True):
                cont += 1
                done = False
        if(cont > len(lineas)-2):
            break
    print(time.time() - inicio)