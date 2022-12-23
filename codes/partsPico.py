"""
This is the code of the constituent components of the Raspberry Pi Pico control ECT
include：
    1.Two-axis gimbal
    2.Serial communication
    3.buzzer
author:nowloady
email:2225649558@qq.com
version:1.0
2022/12/23
"""
import math
import time

from machine import Pin, PWM, UART


class Gimbal:
    def __init__(self, servoPins, shooterPos=None, camPos=None):  # servoPins = [Pin(22), Pin(23)]
        # ---Initialize the variable--- #
        if camPos is None:
            camPos = [0, 0, 0]
        if shooterPos is None:
            shooterPos = [0, 0, 0]
        self.shooterPos = shooterPos
        self.camPos = camPos
        self.servoPWMs = [PWM(servoPins[0]), PWM(servoPins[1])]
        for pwm in self.servoPWMs:
            pwm.freq(50)
        # ---Process variables--- #
        self.Angles = [90.0, 90.0]  # degrees
        # ---Initialize Servos--- #
        for i in range(2):
            self.servoPWMs[i].duty_u16(int(((self.Angles[i] / 180 * 2 + 0.5) / 20) * 65535))
        print("[log]: class Gimbal is ok")

    def calc2aim(self, x, y, d):  # Gimbal coordinates (this function may cause problems)
        POS = []
        for i, var in enumerate([x, y, d]):
            POS.append(var + [0, 0, 0] - [0, 0, 0])  # 计算 adapted 列表中的每个元素
        self.Angles[0] = math.degrees(math.pi / 2 - math.atan(POS[0] / POS[2]) * 0.4)
        self.Angles[1] = math.degrees(math.pi / 2 - math.atan(
            POS[1] / math.sqrt(POS[0] ** 2 + POS[2] ** 2)) * 0.4)
        for i in range(2):
            self.servoPWMs[i].duty_u16(int(((self.Angles[i] / 180 * 2 + 0.5) / 20) * 65535))

    def adjust(self, X, Y):
        self.Angles[0] += X
        self.Angles[1] += Y
        for i, angle in enumerate(self.Angles):
            self.servoPWMs[i].duty_u16(int(((angle / 180 * 2 + 0.5) / 20) * 65535))


class PicoUART:
    def __init__(self, channel, Baud, tx, rx):
        self.uart = UART(channel, Baud, tx=Pin(tx), rx=Pin(rx))
        self.channel = channel
        self.write("uart ok")
        print("[log]: class PicoUART is ok")

    def read(self):
        if self.uart.any():
            cmdline = self.uart.read()
            if cmdline is not None:
                try:
                    cmdline_str = cmdline.decode('utf-8', 'ignore').replace('\r', '').replace(' ', '')
                    strs = cmdline_str.split('\n')
                    if strs[len(strs) - 1] == '':
                        strs.pop()
                    return strs
                except:
                    print("UART read wrong")
                    return None

    def write(self, message):
        self.uart.write(message)
        pass


class Beep:
    def __init__(self, Pin):
        self.beep = PWM(Pin)
        self.setTone()
        self.setVolume(10)
        time.sleep(1)
        self.setVolume(0)

    def setTone(self, fre=262):
        self.beep.freq(int(fre))

    def setVolume(self, percentage=0):
        self.beep.duty_u16(int(percentage / 100 * 65535))
