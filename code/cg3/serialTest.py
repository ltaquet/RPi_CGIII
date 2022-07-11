import serial
import time
import os

ser=serial.Serial('/dev/ttyUSB1',115200)

ser.write(b"1S")

time.sleep(2)

ser.write(b"!!!")


#os.system("cat /dev/ttyUSB0  >> ../../data/myfile.txt")

print(ser.inWaiting())

for x in range(90):
	readedText = ser.readline()
	print(readedText)

ser.close()

