import serial
import serial.tools.list_ports
import numpy as np


class SerialManager:
    serial_port = None
    
    def __init__(self):
        pass

    def open_serial(self, port):
        try:
            self.serial_port = serial.Serial(port, 115200, timeout = 0.1)
            print("opening")
        except ValueError as e:
            print(e)
        except FileNotFoundError:
            print("Invalid COM port.")
            return False
        except IOError as e:
            print(e)
        return True

    def communicate(self, command):
        try:
            self.serial_port.write(bytes(command, 'utf-8'))
            
            back_val = None
            while back_val == None: back_val = self.serial_port.readline()
            print(back_val)

        except Exception as e:
            print(e)

    def establish_connection(self):
        connected = False
        try:
            while(not connected):
                if(self.serial_port.is_open):
                    arduino_handshake = self.serial_port.read().decode('utf-8')
                    print(arduino_handshake)
                else: continue
                if(arduino_handshake == 'C'):
                    connected = True
        except Exception as e:
            print(e)

    def start(self, port):
        if not self.open_serial(port):
            print("not")
            return False
        print('opened')
        self.establish_connection()
        return True

    def close(self):
        try:
            self.serial_port.close()
        except Exception as e:
            print(e)

    def get_ports(self):
        com_list = serial.tools.list_ports.comports()
        for i in range(0, len(com_list)):
            com_list[i] = com_list[i].device
        return com_list