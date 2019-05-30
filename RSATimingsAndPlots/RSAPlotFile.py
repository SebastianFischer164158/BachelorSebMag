import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
#import seaborn as sns
plt.style.use("seaborn-darkgrid")
ESP32xtick = np.arange(40,621,20) #number of decimals
ESP32ytick = np.arange(0,330000,25000)
#@@@@@@@@@@@@@@@@@@@@ DATA @@@@@@@@@@@@@@@@@@@@#
keysizes_ESP32 = np.array([40,60,80,100,120,
                          140,155,160,180,200,
                          220,240,260,280,300,
                          309,320,340,360,380,
                          400,420,440,460,480,
                          500,520,540,560,580,
                          600,617,620]) #155 is 512RSA, 309 is RSA 1024, 617 is 2048 RSA

keygen_time_ESP32 = np.array([2,2,3,3,4,4,3,5,6,6,5,6,6,6,6,7,10,11,12,11,12,12,13,13,13,15,14,14,15,15,16,16,16]) #unit in ms

keygen_time_UNO = np.array([21])
keygen_time_ESP8266 = np.array([3, 4, 5])
keygen_time_MEGA = np.array([21, 28, 40, 49, 60, 69, 74, 86, 97, 104, 114])


encrypt_times_ESP32 = np.array([11, 19, 34, 47, 57,
                                67, 74, 101, 122, 135, 152,
                                164, 180, 199, 214, 223, 304,
                                348, 361, 390, 401, 431,
                                448, 480, 512, 529, 550,
                                575, 596, 612, 635, 651, 657]) #unit in ms
encrypt_times_UNO = np.array([427])
encrypt_times_ESP8266 = np.array([39, 77, 124])
encrypt_times_MEGA = np.array([432, 877, 1374, 2004, 2692, 3390, 4150, 4451, 5462, 6375, 7537])

decryption_times_ESP32 = np.array([160, 447, 1188, 2254, 3287,
                                   4717, 5841, 8523, 12153, 14976, 18679,
                                   22360, 27233, 33423, 38386, 41984, 61677,
                                   74499, 84099, 94113, 103109, 118499,
                                   131548, 148389, 164413, 178871, 197647,
                                   214849, 235389, 251535, 276178, 290122, 294126]) #unit in ms

decryption_times_UNO = np.array([]) #could not decrypt
decryption_times_ESP8266 = np.array([427, 1932])
decryption_times_MEGA = np.array([7159, 22086, 50114, 99094, 161963, 248439, 330782, 380820, 550030, 723120, 958844])



#@@@@@@@@@@@@@@@@@@@@ PLOTS @@@@@@@@@@@@@@@@@@@@#


#plt.plot(encrypt_times_ESP32,keysizes_ESP32)
#plt.plot(keysizes_ESP32,decryption_times_ESP32)

#plt.plot(keysizes_ESP32,keygen_time_ESP32)



#@@@@@@@@@@@@@@@@@@@@ KEY SIZS VS DECRYPTION TIMES @@@@@@@@@@@@@@@@@@@@#

#### RSA_ESP32_KeySize VS decryptionTime ####

fig2, ax2 = plt.subplots(1,figsize=(12,9))
ax2.plot(keysizes_ESP32,decryption_times_ESP32,'k')
ax2.axhline(y=5841, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax2.axhline(y=41984, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax2.axhline(y=290122, color='gray', linestyle=':') #RSA-2048 (617 decimals)
ax2.text(655,5841, "RSA-512", va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5))
ax2.text(-11,5841, "5841")
ax2.text(655,41984, "RSA-1024", va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5))
ax2.text(-18,41984, "41984")
ax2.text(655,290122, "RSA-2048", va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5))
ax2.text(-24,290122, "290122")
ax2.set_ylabel('[ms]', fontsize=10)
ax2.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(ESP32xtick)
plt.yticks(ESP32ytick)

plt.plot(155, 5841, 'xr')
plt.plot(309, 41984, 'xr')
plt.plot(617, 290122, 'xr')


#### RSA_KeySize VS decryptionTimeUNO ####
#UNO could not handle it.

#### RSA_KeySize VS decryptionTimeESP8266 ####
ESP8266xtick = np.arange(40,62,2)
fig3, ax3 = plt.subplots(1,figsize=(12,9))
ax3.plot(ESP32xtick[0:2],decryption_times_ESP8266,'k') #only two datapoints, talk about this.
ax3.set_xticks(ESP8266xtick)
ax3.set_ylabel('[ms]', fontsize=10)
ax3.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')

#### RSA_KeySize VS decryptionTimeMEGA####
fig4, ax4 = plt.subplots(1,figsize=(12,9))
ax4.plot(keysizes_ESP32[0:11],decryption_times_MEGA,'k') #only two datapoints, talk about this.
#ax4.set_xticks(ESP8266xtick)
ax4.axhline(y=330782, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax4.text(231,330782, "RSA-512", va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5))

ax4.set_ylabel('[ms]', fontsize=10)
ax4.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
ax4.plot(155, 330782, 'xr')
ax4.text(29,330782, "330782")

#@@@@@@@@@@@@@@@@@@@@ KEY SIZS VS DECRYPTION TIMES @@@@@@@@@@@@@@@@@@@@#


plt.show()
