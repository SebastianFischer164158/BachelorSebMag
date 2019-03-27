import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
plt.style.use("seaborn-darkgrid")

#fig, ax = plt.subplots(1,figsize=(12,9))

#@@@@@@@@@@@@@@@@@@@@ DATA @@@@@@@@@@@@@@@@@@@@#
ESP32xtick = np.arange(40,621,20) #number of decimals
ESP32ytick = np.arange(0,330000,25000)
keysizes_ESP32 = np.array([40,60,80,100,120,
                          140,155,160,180,200,
                          220,240,260,280,300,
                          309,320,340,360,380,
                          400,420,440,460,480,
                          500,520,540,560,580,
                          600,617,620]) #155 is 512RSA, 309 is RSA 1024, 617 is 2048 RSA

encrypt_times_ESP32 = np.array([11, 19, 34, 47, 57,
                                67, 74, 101, 122, 135, 152,
                                164, 180, 199, 214, 223, 304,
                                348, 361, 390, 401, 431,
                                448, 480, 512, 529, 550,
                                575, 596, 612, 635, 651, 657]) #unit in ms

decryption_times_ESP32 = np.array([160, 447, 1188, 2254, 3287,
                                   4717, 5841, 8523, 12153, 14976, 18679,
                                   22360, 27233, 33423, 38386, 41984, 61677,
                                   74499, 84099, 94113, 103109, 118499,
                                   131548, 148389, 164413, 178871, 197647,
                                   214849, 235389, 251535, 276178, 290122, 294126]) #unit in ms

keygen_time_ESP32 = np.array([2,3,3,4,4,
                              4,4,6,6,6,5,
                              6,6,6,7,8,10,
                              11,12,12,12,13,
                              13,13,13,15,15,
                              15,15,15,16,17, 17]) #unit in ms


#plt.plot(encrypt_times_ESP32,keysizes_ESP32)
#plt.plot(keysizes_ESP32,decryption_times_ESP32)

#plt.plot(keysizes_ESP32,keygen_time_ESP32)


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

y1 = 5841
plt.plot(155, 5841, 'xr')
plt.plot(309, 41984, 'xr')
plt.plot(617, 290122, 'xr')
plt.show()
