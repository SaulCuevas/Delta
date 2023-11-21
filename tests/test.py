from Comunicacion import ESP32_serial
import time

ESP32 = ESP32_serial.start_serial()
inicio = time.time()
ESP32_serial.enviar_trayectoria(ESP32)
print(time.time()-inicio)
ESP32_serial.stop_serial(ESP32)