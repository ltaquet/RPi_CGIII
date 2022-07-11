
import sys
import CyberGlove
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)
TTLpin = 31

GPIO.setup(TTLpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

data_dir = "../../data/" 
PID = sys.argv[1]
data_dir = data_dir + PID + "/"

ll = 0;
last = 0;
curr = 0;
stream = False
running = True
recordings = 0;

loop = 0
stuck = 0

runningSum = 0;

s = CyberGlove.CyberGlove()

file_obj = open(data_dir + PID + s.timestamp() +"_Log","w")
TTL = open(data_dir + PID + s.timestamp() +  "_TTL","w")

file_obj.write("Good Clock," + s.timestamp() + "\n")
s.device.write(bytes(b'1tg'));

sleep(2)

s.device.read(3)
TS = (s.device.read(11)).decode('utf-8')
print(TS)
file_obj.write("CyberGlove Clock," + TS  + "\n")

s.device.read(s.device.inWaiting())
#file_obj.write("CyberGlove Clock, " + (s.device.read(15)).decode('utf-8') + "\n")
#print(s.device.inWaiting())
#print((s.device.read(14)).decode('utf-8'))

print("READY")

filename = "placeholder"

while(running):
    loop = loop + 1
    sleep(0.001)
    ll = last;
    last = curr

    if loop == 1:
        file_obj.write("TTL Sampling Started," + s.timestamp()+ "\n")
        
    curr = GPIO.input(TTLpin)
    TTL.write(str(curr)+",")
    if stream:
        s.read_all("../../data/" + PID + "/" + PID + "_" + filename)
        
    if not stream and last == 1 and curr == 0:
        stream = not stream
        filename = s.stream()
        cmdSent = s.timestamp()
        file_obj.write("CyberGlove Start," + filename + "\n")
        file_obj.write("Cmd Sent," + cmdSent + "\n")
        print("streaming " + str(loop))
        #print(filename)
        while(curr != 0 or last != 0 or ll != 0):
            sleep(0.001)
            ll = last
            last = curr
            curr = GPIO.input(TTLpin)
            TTL.write(str(curr)+",")

        
    elif stream and last == 0 and curr == 1:
        stream = not stream
        file_obj.write("CyberGlove Stop," + s.stop_stream() + "\n")
        print("Stopping stream " + str(loop)+ "\n")
        sleep(0.5)
        s.read_all("../../data/" + PID + "/" + PID + "_" + filename)
        s.device.read(s.device.inWaiting())
        recordings = recordings+1
        print(recordings)
        if 1000 > (os.path.getsize("../../data/" + PID + "/" + PID + "_" + filename)):
            print("WARNING: FILESIZE LOW")
        while(curr != 0 or last != 0 or ll != 0):
            sleep(0.001)
            ll = last
            last = curr
            curr = GPIO.input(TTLpin)
            TTL.write(str(curr)+",")

            runningSum = runningSum + 1;
            if runningSum > 2000:
                s.StopCG()
                file_obj.write("TTL Sampling Ended," + s.timestamp())
                file_obj.close()
                TTL.close()
                print("Closed CyberGlove")
                running = False
                
                runningSum = 0
                
        runningSum = 0;
#        print(last)
#        print(curr)

        
    
#    if GPIO.input(TTLpin)==1:
#        print("Button was pressed:")
#        sleep(.1)


