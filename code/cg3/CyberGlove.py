import serial 
import GoodClock
import time

stopPacket = bytearray()
stopPacket.append(0x03)

w1_1 = bytearray()
w1_1.append(0xA)

w1_2 = bytearray()
w1_1.append(0x00)

w2_1 = bytearray()
w2_1.append(0x00)

w2_2 = bytearray()
w2_1.append(0x02)

startPacket = bytes(b'1S');

uPacket = bytearray()
uPacket.append(0x01)

class CyberGlove:

        def __init__(self):
                self.port = '/dev/ttyUSB0'
                self.baud = 115200
                self.device = serial.Serial(self.port,self.baud)
                time.sleep(3)
                self.device.write(bytes(b'!!!'))
                self.device.write(bytes(b'G'))
                time.sleep(1)
                self.device.write(bytes(b'1ds'))
                time.sleep(1)
                self.device.write(bytes(b'1eu'))
                time.sleep(1)
                self.device.write(bytes(b'1dw'))
                time.sleep(1)
                self.device.write(bytes(b'1u'))
                self.device.write(uPacket)
                time.sleep(1)
                self.device.write(bytes(b'1m'))
                self.device.write(stopPacket)
                
                
                self.device.flush()
                self.Clock = GoodClock.GoodClock()
                self.Clock.run()
                time.sleep(1)

                while (self.Clock.now() == None:
                       print('No fix yet')
                       time.sleep(6)
                print('Got fix: ' + str(self.Clock.now()))

                while (str(self.Clock.now().strftime("%f")) != "000000"):
                        pass
                
                self.device.write(bytes(b'1ts'))
                self.device.write(str(self.Clock.now().strftime("%H:%M:%S")).encode('utf-8'))
                #print(str(self.Clock.now().strftime("%H:%M:%S")))
                time.sleep(1)
                self.device.write(bytes(b'1tg'))
                print(str(self.Clock.now().strftime("%H:%M:%S.%f")))
                print(self.device.read(self.device.inWaiting()))
                time.sleep(1)


        def timestamp(self):
                return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))
        def stream(self):
                self.device.write(startPacket)
#                print(type(self.Clock.now()))

                return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))
        def stop_stream(self):
                self.device.write(stopPacket)
                return str(self.Clock.now().strftime("%Y_%m_%d___%H_%M_%S_%f"))
                
                
        def read_all(self, f1):
                file_obj = open(f1,"ab")
                
                while self.device.inWaiting() > 58:
                        file_obj.write(self.device.readline())
                        
                file_obj.close()

        def dump(self):
                while self.device.inWaiting() != 0:
                        self.device.read(self.device.inWaiting());
                        
                        
                
                
        def StopCG(self):
                self.device.close()

                
