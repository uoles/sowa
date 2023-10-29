#!/usr/bin/python3
from pymodbus.client.serial import ModbusSerialClient as ModbusClient


class Controller:

    isWingDown = True

    def __init__(self):
        self.client = ModbusClient(method='rtu', port='/dev/ttyACM0', baudrate=230000, timeout=1.5)
        self.client.connect()

    # отправить значение в контроллер крыла совы
    def send_value(self, value):
        print('send new value: ' + str(value))
        self.client.write_register(address=0x0000, value=value, slave=0x01)

    # поднять крыло совы
    def sowa_wing_up(self):
        self.send_value(100)
        self.isWingDown = False

    # опустить крыло совы
    def sowa_wing_down(self):
        self.send_value(0)
        self.isWingDown = True
        print('=======================================')

    def close(self):
        self.client.close()

    def is_wing_down(self):
        return self.isWingDown