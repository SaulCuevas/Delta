import smbus
import math

bus = smbus.SMBus(1)

MT_DEVICE_ADDRESS = 6

def bin2dec(binary):
    return sum( val*(2**idx) for idx, val in enumerate(reversed(binary)))

def Lectura_MT6701():
    slaveByte1 = bus.read_i2c_block_data(MT_DEVICE_ADDRESS, 3)
    slaveByte2 = bus.read_i2c_block_data(MT_DEVICE_ADDRESS, 4)
    concat = bin2dec(slaveByte1 + slaveByte2[:-2])
    return concat*2*math.pi / 16384

print(Lectura_MT6701())