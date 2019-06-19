#!/usr/bin/python
# coding=utf-8

iface = "wlan0mon"
from scapy.all import *
from subprocess import check_output
print("SCAPY VERSION USED: "+ scapy._version())
print("Python Version Used: "+ sys.version)

####Test til at sniffe UDP pakker fra SCS. 

def setMonitorMode():

    checkphrase_mon_success = "monitor mode vif enabled"
    checkphrase_mon = "Mode:Monitor"

    moncheck = check_output(["iwconfig"],stderr=subprocess.PIPE).decode("UTF-8") #stderr=subprocess.PIPE simply "silences" the output.

    if checkphrase_mon in moncheck:
        print("wlan0mon is already in Monitor Mode!")

    else:
        airmoncheck = check_output(["airmon-ng", "start", "wlan0"],stderr=subprocess.PIPE).decode("UTF-8")
        if checkphrase_mon_success in airmoncheck:
            print("Sucessfully set wlan0 to Monitor Mode (now called wlan0mon)!")
        else:
            raise SystemExit("wlan0 has not entered Monitor Mode, recheck.")

setMonitorMode()
counter = 0
def handlepackets(frame):
    global counter

    if frame.haslayer(UDP):
        print("- - - - FOUND UDP PACKET - - - - ")
        #print(frame.show())
        try:
            payload = frame[Raw].load
            counter +=1

            print("Payload is: "+ payload)
            print("Src: "+ frame[IP].src) #syntax er frame[LAYER].etfield
            print("Dst: "+ frame[IP].dst)

            frame.pdfdump(str(counter)+"packet.pdf")
        except IndexError as e:
            print("No Payload in Packet")
            pass






sniff(iface="wlan0mon",count=0, prn = handlepackets)
print("ENDED")
