import datetime
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
        self.antenna_length = ""
        self.antenna_location = ""

        self.data = []

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
        if(int(start_freq) >= self.stop_freq):
            print("ERROR: Start frequency must be lesser than stop frequency")
            return

        self.start_freq = int(start_freq)
        self.ser.write((str(self.start_freq) + 'a').encode('utf-8'))

    def set_stop_freq(self, stop_freq = 27000000):
        if(int(stop_freq) <= self.start_freq):
            print("ERROR: Stop frequency must be greater than start frequency")
            return

        self.stop_freq = int(stop_freq)
        self.ser.write((str(self.stop_freq) + 'b').encode('utf-8'))

    def set_steps(self, steps = 20):
        if(int(steps) < 2):
            print("ERROR: Number of steps must be greater than '1'")
            return
        self.steps = int(steps)
        self.ser.write((str(self.steps) + 'n').encode('utf-8'))

    def fetch_data(self):
        self.ser.write('s'.encode('utf-8'))

        self.data = []
        while(True):
            tmp = self.ser.readline().decode('utf-8')
            if tmp == "":
                break
            self.data.append(tmp)

    def plot(self):
        self.fetch_data()
        #self.reader = csv.reader(self.data.splitlines(True), delimiter=',')
        self.reader = csv.reader(self.data, delimiter=',')
        x = []
        y = []

        for row in self.reader:
            print(row)
            if(row[0].upper() != "END"):
                x.append(row[0])
                y.append(row[2])

        #x = np.arange(self.start_freq, self.stop_freq, (self.stop_freq - self.start_freq) / len(y))

        plt.plot(x, y)
        plt.grid()
        #plt.axis('equal')
        plt.xlabel('Frequency in Hz')
        plt.ylabel('SWR')
        plt.ticklabel_format(style='plain', axis='x')

        title = 'VSWR'
        if self.antenna_location != "":
            title = title + " - Antenna Location: " + self.antenna_location
        if self.antenna_length != "":
            title = title + " - Antenna Length: " + self.antenna_length + 'mm'

        title = title + "\nDatetime: " + str(datetime.datetime.now())
        plt.title(title)
        #plt.figtext(0.2, 0.2, "test", bbox=dict(facecolor='red', alpha=0.5))

        plt.show()

    def get_current_settings(self):
        self.ser.write('?'.encode('utf-8'))
        data = ""
        while(True):
            tmp = self.ser.readline().decode('utf-8')
            if tmp == "":
                break
            data = data + tmp

        data = data + 'Antenna location: ' + self.antenna_location + '\n'
        data = data + 'Antenna length: ' + self.antenna_length
        return data

    def save(self):
        pass
        #self.reader = csv.reader(self.data, delimiter=',')
        #for row in self.reader:
        #    print(row)

    def set_antenna_length( self, antenna_length):
        self.antenna_length = antenna_length

    def set_antenna_location(self, antenna_location):
        self.antenna_location = antenna_location

if __name__ == '__main__':
    vna = VnaClient()

    instructions = """
    [a] - set start frequency
    [b] - set stop frequency
    [h] - set antenna location
    [l] - set antenna length
    [n] - set number of steps
    [p] - plot graph
    [g] - get current settings
    [?] - show help
    [q] - quit
    """

    print(instructions)

    while(1):
        inp = input('Choose: ')
        if(inp == 'a'):
            vna.set_start_freq(input('Frequency in Hz: '))
        if(inp == 'b'):
            vna.set_stop_freq(input('Frequency in Hz: '))
        if(inp == 'h'):
            vna.set_antenna_location(input('Antenna location: '))
        if(inp == 'l'):
            vna.set_antenna_length(input('Antenna length (in mm): '))
        if(inp == 'n'):
            vna.set_steps(input('Number of steps: '))
        if(inp == 'p'):
            vna.plot()
            vna.save()
        if(inp == 'g'):
            print(vna.get_current_settings(), '\n')
        if(inp == '?'):
            print(instructions)
        if(inp == 'q'):
            break

    vna.ser.close()
