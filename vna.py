import serial
import csv

import matplotlib.pyplot as plt
import numpy as np

class VnaClient():

    def __init__(self):
        self.ser = serial.Serial(
                #port='/dev/ttyUSB0',
                port='/dev/pts/5',
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5
                )

        self.start_freq = 23000000
        self.end_freq = 27000000

        print('Connection is open:', self.ser.is_open)

        s = self.ser.read(2500)
        #print(s)

        self.ser.write((str(self.start_freq) + 'a').encode('utf-8'))
        self.ser.write((str(self.end_freq) + 'b').encode('utf-8'))
        self.ser.write('20n'.encode('utf-8'))

    def plot(self):
        self.ser.write('s'.encode('utf-8'))
        s = self.ser.read(6500)
        data = s.decode('utf-8')
        #print(data)

        reader = csv.reader(data.splitlines(True), delimiter=',')
        y = []

        for row in reader:
            print(row)
            if(row[0].upper() != "END"):
                y.append(row[2])

        x = np.arange(self.start_freq, self.end_freq, (self.end_freq - self.start_freq) / len(y))

        plt.plot(x, y)
        plt.title('VSWR')

        plt.show()


if __name__ == '__main__':
    vna = VnaClient()
    vna.plot()
    vna.ser.close()
