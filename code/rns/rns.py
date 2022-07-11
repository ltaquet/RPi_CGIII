import serial
import GoodClock
import time

stopPacket = bytearray()
stopPacket.append(0x03)

class rns:

        def __init__(self):
                self.port = '/dev/ttyUSB0'
                self.baud = 115200
                self.device = serial.Serial(self.port,self.baud)
                time.sleep(1)

                self.device.flush()
                self.Clock = GoodClock.GoodClock()
                self.Clock.run()
                time.sleep(1)

                while (self.Clock.now() == None:
                       print('No fix yet')
                       time.sleep(3)
                print('Got fix: ' + str(self.Clock.now()))

        def startECoG(self):
            self.device.write(bytes(b'Z'))
            return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))

        def markECoG(self):
            self.device.write(bytes(b'T'))
            return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))
            
        def stopECoG(self):
            self.device.write(bytes(b'X'))
            return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))
