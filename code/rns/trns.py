import sys
import rns
from time import sleep
import RPi.GPIO as GPIO
import os



############################### DIRECTORY SETUP ###############################
data_dir = "../../data/"
PID = sys.argv[1]
data_dir = data_dir + PID + "/"

################################ VARIABLE INIT ################################
running = True
stream = False;
marks = 0;

s = rns.rns()

logname = data_dir + PID + s.timestamp() +"_Log"

def startMark(channel):
    global stream
    global filename
    global logname
    
    #filename contains GoodClock Timestamp
    markTimestamp = s.markECoG()
    
    file_obj = open(logname,"a")
    
    #Writes GoodClock timestamp that occurs write before glove starts
    file_obj.write("ECoG Mark," + filename + "\n")
    file_obj.close()
    
    GPIO.remove_event_detect(TTLpin)
    GPIO.add_event_detect(TTLpin, GPIO.RISING, callback=endMark)

    return

def endMark(channel):
    global stream
    global filename
    global logname

    markTimestamp = s.markECoG();
    
    file_obj = open(logname,"a")

    #Writes GoodClock timestamp that occurs write before glove starts
    file_obj.write("ECoG Mark," + markTimestamp + "\n")
    file_obj.close()

    GPIO.remove_event_detect(TTLpin)
    GPIO.add_event_detect(TTLpin, GPIO.FALLING, callback=startMark)

    return

def startRNS:

    global stream
    global filename
    global logname

    startTimestamp = s.startECoG

    file_obj.write("ECoG Start," + startTimestamp + "\n")
    file_obj.close()

    GPIO.remove_event_detect(TTLpin)
    GPIO.add_event_detect(TTLpin, GPIO.FALLING, callback=startMark)

    return

    
def halt_recording(channel):
    global stream
    global recordings
    global PID
    global filename
    global logname
    
    #Writes GoodClock timestamp that occurs write after glove stops
    #print(s.stop_stream())
    file_obj = open(logname,"a")
    file_obj.write("CyberGlove Stop," + s.stop_stream() + "\n")
    file_obj.close()
    
    print("Stopping stream")

    #Reads all data still in input serial buffer
    sleep(0.5)
    s.read_all("../../data/" + PID + "/" + PID + "_" + filename)

    #Dumps partial samples
    s.device.read(s.device.inWaiting())

    #Tracks total number of recordings
    recordings = recordings+1
    print(recordings)

    stream = not stream

    #Warning if last recording was unusually small
    if 1000 > (os.path.getsize("../../data/" + PID + "/" + PID + "_" \
                               + filename)):
        print("WARNING: FILESIZE LOW")

    GPIO.remove_event_detect(TTLpin)
    GPIO.add_event_detect(TTLpin, GPIO.FALLING, callback=record)

    return


################################# GPIO SETUP ##################################
GPIO.setmode(GPIO.BOARD)
TTLpin = 31
GPIO.setup(TTLpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
file_obj = open(logname,"a")




################################ MAIN LOOP SETUP ##############################

# Compare GoodClock and CyberGlove Clock post initializtion
file_obj.write("Good Clock," + s.timestamp() + "\n") #write goodclock to log
s.device.write(bytes(b'1tg'));
sleep(2) # Wait for response
s.device.read(3) #Dump 1tg response
TS = (s.device.read(11)).decode('utf-8') #read timestamp
print(TS)


file_obj.write("CyberGlove Clock," + TS  + "\n") #write cyberglove clock to log

#Flush serial input 
s.device.read(s.device.inWaiting())

print("READY")

filename = "placeholder"


################################## MAIN LOOP  #################################

file_obj.close()
GPIO.add_event_detect(TTLpin, GPIO.FALLING, callback=record)
while(running):
    if stream:
         s.read_all("../../data/" + PID + "/" + PID + "_" + filename)

