"""
This is the code for the Raspberry Pi Pico control ECT
author:NowLoadY
email:2225649558@qq.com
version:1.0
2022/12/23
"""
from machine import Pin
import partsPico
import time


class ElectromagneticFort:
    def __init__(self, chargePin, shootPin, GimbalServoPins, UART2PCPins, BeepPin):
        self.chargePin = Pin(chargePin, Pin.OUT)
        self.shootPin = Pin(shootPin, Pin.OUT)
        self.FortGimbal = partsPico.Gimbal([Pin(GimbalServoPins[0]), Pin(GimbalServoPins[1])])
        self.Uart2PC = partsPico.PicoUART(1, 115200, UART2PCPins[0], UART2PCPins[1])
        self.Beep = partsPico.Beep(Pin(BeepPin))
        time.sleep(3)
        # ---过程状态--- #
        self.charged = False

    def charge(self):
        self.chargePin.value(1)
        self.shootPin.value(0)
        self.Beep.setVolume(1)
        for i in range(14):
            self.Beep.setVolume(1)
            time.sleep(0.5)  # Wait 15 seconds for charging
            self.Beep.setVolume(0)
            time.sleep(0.5)
        self.Beep.setTone()
        self.Beep.setVolume(0)
        time.sleep(0.5)
        self.Beep.setVolume(1)
        time.sleep(0.2)
        self.Beep.setVolume(0)
        time.sleep(0.2)
        self.Beep.setVolume(1)
        time.sleep(0.2)

        self.charged = True

    def wait(self):
        self.Beep.setTone()
        self.Beep.setVolume()
        self.chargePin.value(0)
        self.shootPin.value(0)

    def shoot(self):
        self.Beep.setTone(500)
        self.Beep.setVolume(1)
        self.chargePin.value(0)
        self.shootPin.value(1)
        time.sleep(0.5)
        self.Beep.setTone()
        self.Beep.setVolume(0)
        self.charged = False

    def handleCMDS(self, CMDS_STR):
        if CMDS_STR is not None:
            try:
                last_command = CMDS_STR[len(CMDS_STR) - 1]
                vals = last_command.split('|')
                if vals[0] == 'AC':  # Aim by calculation
                    self.FortGimbal.calc2aim(float(vals[1]), float(vals[2]), float(vals[3]))
                elif vals[0] == 'AA':  # Fine-tuning
                    self.FortGimbal.adjust(float(vals[1]), float(vals[2]))
                elif vals[0] == 'ST':  # shoot
                    if self.charged:
                        self.shoot()
                    else:
                        self.charge()
                        self.shoot()
                    self.wait()
            except:
                print("Error occurred while parsing command: %s", CMDS_STR)


# ----The power-on status LED would blink for once---- #
led = Pin(25, Pin.OUT)
led.high()
time.sleep(1)
led.low()
time.sleep(1)
print("[log]: start up")
# ----开始构建---- #
Num_chargePin = 18
Num_shootPin = 19
Num_GimbalServoPins = [20, 21]
#Num_TOF050FPins = [4, 5]
Num_UART2PCPins = [8, 9]
Num_BeepPin = 22

MyElectromagneticFort = ElectromagneticFort(chargePin=Num_chargePin,
                                            shootPin=Num_shootPin,
                                            GimbalServoPins=Num_GimbalServoPins,
                                            UART2PCPins=Num_UART2PCPins,
                                            BeepPin=Num_BeepPin)
#MyElectromagneticFort.charge()
MyElectromagneticFort.wait()
# ----start loop---- #
print("[log]: start loop")
while True:
    commands = MyElectromagneticFort.Uart2PC.read()
    time.sleep(0.001)
    if commands is not None:
        MyElectromagneticFort.handleCMDS(commands)
