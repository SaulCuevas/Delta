import sys

sys.path.append("../Delta")

from Comunicacion import ESP32_serial

ser = ESP32_serial.start_serial()
ESP32_serial.enviar_trayectoria(ser)
ESP32_serial.stop_serial(ser)