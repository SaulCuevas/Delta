import sys
import time

sys.path.append("../Delta")

from Comunicacion import ESP32_serial
Ki = 2
Ki_arriba = 5

ser = ESP32_serial.start_serial()

for x in range(10):
    ESP32_serial.cambiarK(ser, K=Ki_arriba, motor=0, valor=x)
    ESP32_serial.cambiarK(ser, K=Ki_arriba, motor=1, valor=x)
    ESP32_serial.cambiarK(ser, K=Ki_arriba, motor=2, valor=x)
    print("--- K's actulizadas ---")
    time.sleep(5)
    ESP32_serial.enviar_trayectoria(ser)
    time.sleep(10)

ESP32_serial.stop_serial(ser)