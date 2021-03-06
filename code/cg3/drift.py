import sys
import CyberGlove
from time import sleep

s = CyberGlove.CyberGlove()


file_obj = open("tests/"+s.timestamp() +"_Log","w")

file_obj.write("Good Clock," + s.timestamp() + "\n")
s.device.write(bytes(b'1tg'));

sleep(2)

s.device.read(3)
TS = (s.device.read(11)).decode('utf-8')
s.device.read(s.device.inWaiting())

file_obj.write("CyberGlove Clock," + TS  + "\n")

loops = 0

while(1):

    print(loops)
    start = s.stream();
    file_obj.write("CyberGlove Start," + start + "\n")
    sleep(5)
    s.stop_stream()
    sleep(0.5)
    s.device.read(2)
    file_obj.write(s.device.read(14).decode('utf-8')+"\n")
    
    
    sleep(1)
    s.read_all("tests/junk_"+s.timestamp())
    sleep(2)
    s.dump()
    
    loops = loops + 1

     
    
