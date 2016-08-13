import serial
import csv

import matplotlib.pyplot as plt
import numpy as np

class VnaClient():
    def __init__(self):
        self.ser = serial.Serial(
                #port='/dev/ttyUSB0',
                port='/dev/pts/2',
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5
                )

        self.start_freq = 23000000
        self.stop_freq = 27000000
        self.steps = 20

        print('Connection is open:', self.ser.is_open)

        s = ""
        while(True):
            tmp = self.ser.readline().decode('utf-8')
            s = s + tmp
            if tmp == "":
                break

        print(s)

        self.set_start_freq()
        self.set_stop_freq()
        self.set_steps()

    def set_start_freq(self, start_freq = 23000000):
        self.start_freq = int(start_freq)
        self.ser.write((str(self.start_freq) + 'a').encode('utf-8'))

    def set_stop_freq(self, stop_freq = 27000000):
        self.stop_freq = int(stop_freq)
        self.ser.write((str(self.stop_freq) + 'b').encode('utf-8'))

    def set_steps(self, steps = 20):
        self.steps = int(steps)
        self.ser.write((str(self.steps) + 'n').encode('utf-8'))

    def plot(self):
        self.ser.write('s'.encode('utf-8'))

        data = ""
        while(True):
            tmp = self.ser.readline().decode('utf-8')
            data = data + tmp
            if tmp == "":
                break

        reader = csv.reader(data.splitlines(True), delimiter=',')
        y = []

        for row in reader:
            print(row)
            if(row[0].upper() != "END"):
                y.append(row[2])

        x = np.arange(self.start_freq, self.stop_freq, (self.stop_freq - self.start_freq) / len(y))

        plt.plot(x, y)
        plt.title('VSWR')

        plt.show()

    def get_current_settings(self):
        self.ser.write('?'.encode('utf-8'))
        data = ""
        while(True):
            tmp = self.ser.readline().decode('utf-8')
            data = data + tmp
            if tmp == "":
                break
        print(data)

if __name__ == '__main__':
    vna = VnaClient()

    instruction = """
    [a] - set start frequency
    [b] - set stop frequency
    [n] - set number of steps
    [s] - plot graph
    [?] - get current settings
    [q] - quit
    """

    print(instruction)

    while(1):
        inp = input('Choose: ')
        if(inp == 'a'):
            vna.set_start_freq(input('Frequency in Hz: '))
        if(inp == 'b'):
            vna.set_stop_freq(input('Frequency in Hz: '))
        if(inp == 'n'):
            vna.set_steps(input('Number of steps: '))
        if(inp == 's'):
            vna.plot()
        if(inp == '?'):
            vna.get_current_settings()
        if(inp == 'q'):
            break

    vna.ser.close()
