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
#keygen times
keygen_time_ESP32 = np.array([2,2,3,3,4,4,3,5,6,6,5,6,6,6,6,7,10,11,12,11,12,12,13,13,13,15,14,14,15,15,16,16,16]) #unit in ms

keygen_time_MEGA = np.array([21,30,42,50,61,71,75,87,97,105,115,127,137])

keygen_time_UNO = np.array([21,29,41,49])

keygen_time_ESP8266 = np.array([2,2,4,4,4,5,5,6,6,7,6,7,8,9,9,10])

#encryption times
encrypt_times_ESP32 = np.array([9,19,35,48,57,66,75,100,122,133,151,164,182,198,212,222,310,344,365,393,417,
                                433,453,484,513,524,554,573,597,618,644,676,669])

encrypt_times_MEGA = np.array([421,858,1418,2056,2792,3431,4101,4397,5433,6328,7559,
                               8534,10009])

encrypt_times_UNO = np.array([417])

encrypt_times_ESP8266 = np.array([19, 38, 64, 91, 123, 150, 179, 194, 241, 277, 309, 373, 431, 483, 535, 558])

#decryption times
decryption_times_ESP32 = np.array([166,478,1178,2255,3308,4653,5862,8426,
                                   12143,14813,18718,22392,27397,33656,
                                   38497,41682,62494,74225,83056,94298,109358,
                                   119580,133670,147810,164162,177804,
                                   198160,215917,236049,251666,
                                   278582,303105,303245]) #unit in ms

decryption_times_UNO = np.array([]) #could not decrypt

decryption_times_ESP8266 = np.array([320, 964, 2235, 4377, 7074])

decryption_times_MEGA = np.array([4199,22063,50159,99801,162051,248167,331241,381352,
                                  549575,725480,959445,1195498])


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
