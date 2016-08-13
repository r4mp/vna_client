import serial
import struct
import csv

import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5
        )

start_freq = 23000000
end_freq = 27000000

print('Connection is open:', ser.isOpen())

s = ser.read(2500)
#print(s)

ser.write((str(start_freq) + 'a').encode('utf-8'))
ser.write((str(end_freq) + 'b').encode('utf-8'))
ser.write('20n'.encode('utf-8'))

ser.write('s'.encode('utf-8'))
s = ser.read(6500)
data = s.decode('utf-8')
#print(data)

reader = csv.reader(data.splitlines(True), delimiter=',')

for row in reader:
    print(row)

ser.close()

