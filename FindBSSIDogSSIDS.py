#!/usr/bin/env python
# coding=utf-8
from subprocess import check_output
from scapy.all import *
import random

channel_value = 1
ssid_bssid = []
STA_list = []
channel_enganged = False
def setChannel():
    global channel_value
    #channel_value = random.randint(1,14)
    if channel_value == 13:
        channel_value = 1
    else:
        channel_value +=1

    moncheck = check_output(["sudo","iwconfig","wlan0mon","channel",str(channel_value)], stderr=subprocess.PIPE).decode("UTF-8")  # stderr=subprocess.PIPE simply "silences" the output.


def FindSSIDtest(frame):
    setChannel() #we try a random channel every call. nok ikke specielt efficient.
    if frame.haslayer(Dot11): #der kunne bare stå haslayer(Dot11Beacon)
        if frame.type == 0 and frame.subtype == 8: #KUN beacon frames!!
            SSID = frame.info
            BSSID = frame.addr3.upper()
            #print(bssid)
            if (BSSID,SSID) not in ssid_bssid and len(SSID) != 0: #gider ikke hidden SSIDs aka 0 len.
                ssid_bssid.append((BSSID,SSID))
                ch = int(ord(frame[Dot11Elt:3].info))

                print("Found BSSID " + BSSID + " and SSID "+SSID +" on channel: " +str(ch))#addr 3 er bssid (mac addresse for ap) , frame.info er SSID



def FindSTAinSpecificBSSID(bssidsearch,frame,channel):
    global channel_enganged
    if channel_enganged == False:
        moncheck = check_output(["sudo", "iwconfig", "wlan0mon", "channel", str(channel)], stderr=subprocess.PIPE).decode("UTF-8")
        channel_enganged = True


    BSSID = "ff:ff:ff:ff:ff:ff"

    if frame.haslayer(Dot11):
        if frame.type == 2:
            DS = frame.FCfield & 0x03
            toDS = DS & 0x01 != 0
            fromDS = DS & 0x2 != 0


            if toDS == 0 and fromDS == 0:  # dette burde KUN være data frames der sendes til AP.
                RA = DA = frame.addr1.upper()  # RA= REciver, DA = fianl destination
                TA = SA = frame.addr2.upper()
                BSSID = frame.addr3.upper()

            elif toDS == 0 and fromDS == 1:
                RA = DA = frame.addr1.upper()  # RA= REciver, DA = fianl destination
                TA = BSSID = frame.addr2.upper()
                SA = frame.addr3.upper()

            elif toDS == 1 and fromDS == 0:
                RA = BSSID = frame.addr1.upper()
                TA = SA = frame.addr2.upper()
                DA = frame.addr3.upper()

            elif toDS == 1 and fromDS == 1:
                RA = frame.addr1.upper()
                TA = frame.addr2.upper()
                DA = frame.addr3.upper()
                SA = frame.addr4.upper()
            else:
                SA = "ff:ff:ff:ff:ff:ff"  # dette burde ikke kunne ske
                BSSID = "ff:ff:ff:ff:ff:ff"

            if SA not in STA_list and BSSID == bssidsearch:
                STA_list.append(SA)
                #print("VALUE OF toDS = " + str(toDS))
                #print("VALUE OF fromDS = "+str(fromDS))
                print("FOUND NEW STATION: " + SA + " FROM AP: " + BSSID)

            #frame.pdfdump(filename= "frame"+str(i) +".pdf")
            #frame.pdfdump()

iwantit = "40:F2:01:9A:42:56"
sniff(iface="wlan0mon", count=0, prn=FindSSIDtest, store=0) #finds SSIDS


#iwantit = "30:AE:A4:0D:E6:C1"

#sniff(iface="wlan0mon", count=0,prn= lambda fr: FindSTAinSpecificBSSID(iwantit,fr,4),store=0) ## kan gøres uden lambda funktion, men tja. så kald checkframe uden parentser, elle argument.

#sniff(iface="wlan0mon", monitor=True, prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%\t%PrismHeader.channel%\t%Dot11Beacon.cap%}"))
