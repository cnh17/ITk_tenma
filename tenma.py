# imports
import serial
from time import time, sleep


class Tenma:

    """ 
    Remote Control Interface to TENMA power supply
    Tested on TENMA 72-2930 
    """
    
    # initialize object
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 9600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, xonxoff = False, timeout = 0.1):
        self.__record       = {}
        self.__record['V']  = []               # set up tracking of voltage
        self.__record['I']  = []               # set up tracking of current
        self.__range        = {}
        self.__range['V']   = (0.0, 24.0)      # min,max voltage
        self.__range['I']   = (0.0, 10.0)      # min,max current
        self.__time_ref     = time()           # time reference for tracking 
        self.__sleep        = 0.1              # sleep time between read/write to device
        self.__ser          = serial.Serial()  # initialize port
        self.__ser.port     = port             # port name
        self.__ser.baudrate = baudrate         # baud rate
        self.__ser.bytesize = bytesize         # data bit 
        self.__ser.parity   = parity           # parity bit
        self.__ser.stopbits = stopbits         # stop bit
        self.__ser.xonxoff  = xonxoff          # data flow control
        self.__ser.timeout  = timeout          # timeout threshold
        self.__ser.open()                      # open the USB serial port
        print('Serial port is open : ', self.__ser.is_open)
        print('Device name         : ', self.__ser.name)
        self.print_port_config()
        
        
    # generic method to send commands to device
    def __command(self, token, decode_reply = True):
        self.__ser.write( token.encode('utf-8') )
        sleep(self.__sleep)
        if token.endswith('?'):
            reply = self.__ser.read(size = self.__ser.in_waiting)
            sleep(self.__sleep)
            if decode_reply:
                return reply.decode('utf-8').rstrip('\x00')
            else:
                return reply
        
        
    # get value of key ('V', 'I')
    def get_value(self, key, channel = 1):
        token = key + 'SET' + str(channel) + '?'
        return float(self.__command( token ))


    # set value of key ('V', 'I')
    def set_value(self, key, value, channel = 1):
        if value < self.__range[key][0]:
            print('Tenma::set_value(key = \'' + key + '\') : value = ', value, ' is smaller than min = ', self.__range[key][0], ' -- setting value = ', self.__range[key][0])
            value = self.__range[key][0]
        elif value > self.__range[key][1]:
            print('Tenma::set_value(key = \'' + key + '\') : value = ', value, ' is greater than max = ', self.__range[key][1], ' -- setting value = ', self.__range[key][1])
            value = self.__range[key][1]
        token = key + 'SET' + str(channel) + ':' + str(value)
        self.__command( token )
        self.__record[key].append( ((time() - self.__time_ref), value) )
        

    # increment value of key ('V', 'I')
    def increment(self, key, increment, channel = 1):
        value = self.get_value(key, channel) + increment
        self.set_value(key, value, channel)


    # get record for key ('V', 'I')
    def get_record(self, key):
        return self.__record[key]
        

    # print port configuration
    def print_port_config(self):
        print('Tenma serial port settings: \n', self.__ser.get_settings())

