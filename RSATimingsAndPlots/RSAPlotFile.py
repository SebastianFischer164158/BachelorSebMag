import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
plt.style.use("seaborn-darkgrid")
keysizeticks = np.arange(40,621,20)

#keysizeticks = np.array([40,60,80,100,120,140,155,160,
# 180,200,220,240,260,280,300,309,320,340,360,
# 380,400,420,440,460,480,500,520,540,560,580,600,617,620])
#@@@@@@@@@@@@@@@@@@@@ DATA @@@@@@@@@@@@@@@@@@@@#
keysizes = np.array([40,60,80,100,120,
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
decrypt_times_ESP32 = np.array([166,478,1178,2255,3308,4653,5862,8426,
                                   12143,14813,18718,22392,27397,33656,
                                   38497,41682,62494,74225,83056,94298,109358,
                                   119580,133670,147810,164162,177804,
                                   198160,215917,236049,251666,
                                   278582,303105,303245])

decrypt_times_UNO = np.array([]) #could not decrypt

decrypt_times_ESP8266 = np.array([320, 964, 2235, 4377, 7074])

decrypt_times_MEGA = np.array([4199,22063,50159,99801,162051,248167,331241,381352,
                                  549575,725480,959445,1195498])


#@@@@@@@@@@@@@@@@@@@@ PLOTS @@@@@@@@@@@@@@@@@@@@#
#               1 - ESP32 PLOTS
# keysize vs keygen
face_comb = dict(facecolor="w",alpha=0.5)


rsa512_mark_keygen = 3
rsa1024_mark_keygen = 7
rsa2048_mark_keygen = 16
fig1, ax1 = plt.subplots(1,figsize=(12,9))
ax1.plot(keysizes,keygen_time_ESP32)
ax1.axhline(y=rsa512_mark_keygen, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax1.axhline(y=rsa1024_mark_keygen, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax1.axhline(y=rsa2048_mark_keygen, color='gray', linestyle=':') #RSA-2048 (617 decimals)
ax1.text(655,rsa512_mark_keygen, "RSA-512", va='center', ha="left", bbox=face_comb)
#ax1.text(-11,rsa512_mark_keygen, "3")
ax1.text(655,rsa1024_mark_keygen, "RSA-1024", va='center', ha="left", bbox=face_comb)
#ax1.text(-18,rsa1024_mark_keygen, "7")
ax1.text(655,rsa2048_mark_keygen, "RSA-2048", va='center', ha="left", bbox=face_comb)
#ax1.text(-24,rsa2048_mark_keygen, "16")
ax1.set_ylabel('[ms]', fontsize=10)
ax1.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(keysizeticks)
plt.yticks(np.arange(1,17))
plt.plot(np.unique(keysizes), np.poly1d(np.polyfit(keysizes, keygen_time_ESP32, 1))(np.unique(keysizes)),linestyle=':')
plt.plot(155, rsa512_mark_keygen, 'xr')
plt.plot(309, rsa1024_mark_keygen, 'xr')
plt.plot(617, rsa2048_mark_keygen, 'xr')

# keysize vs encryption times
rsa512_mark_encrypt = 75
rsa1024_mark_encrypt = 222
rsa2048_mark_encrypt = 676
fig2, ax2 = plt.subplots(1,figsize=(12,9))
ax2.plot(keysizes,encrypt_times_ESP32)
ax2.axhline(y=rsa512_mark_encrypt, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax2.axhline(y=rsa1024_mark_encrypt, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax2.axhline(y=rsa2048_mark_encrypt, color='gray', linestyle=':') #RSA-2048 (617 decimals)
ax2.text(655,rsa512_mark_encrypt, "RSA-512", va='center', ha="left", bbox=face_comb)
ax2.text(-11,rsa512_mark_encrypt, "75")
ax2.text(655,rsa1024_mark_encrypt, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax2.text(-18,rsa1024_mark_encrypt, "222")
ax2.text(655,rsa2048_mark_encrypt, "RSA-2048", va='center', ha="left", bbox=face_comb)
ax2.text(-24,rsa2048_mark_encrypt, "676")
ax2.set_ylabel('[ms]', fontsize=10)
ax2.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(keysizeticks)
plt.plot(np.unique(keysizes), np.poly1d(np.polyfit(keysizes, encrypt_times_ESP32, 1))(np.unique(keysizes)),linestyle=':')
plt.plot(155, rsa512_mark_encrypt, 'xr')
plt.plot(309, rsa1024_mark_encrypt, 'xr')
plt.plot(617, rsa2048_mark_encrypt, 'xr')

# keysize vs decryption times
rsa512_mark_decrypt = 5862
rsa1024_mark_decrypt = 41682
rsa2048_mark_decrypt = 303105
fig3, ax3 = plt.subplots(1,figsize=(12,9))
ax3.plot(keysizes,decrypt_times_ESP32)
ax3.axhline(y=rsa512_mark_decrypt, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax3.axhline(y=rsa1024_mark_decrypt, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax3.axhline(y=rsa2048_mark_decrypt, color='gray', linestyle=':') #RSA-2048 (617 decimals)
ax3.text(655,rsa512_mark_decrypt, "RSA-512", va='center', ha="left", bbox=face_comb)
ax3.text(-11,rsa512_mark_decrypt, "5862")
ax3.text(655,rsa1024_mark_decrypt, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax3.text(-18,rsa1024_mark_decrypt, "41682")
ax3.text(655,rsa2048_mark_decrypt, "RSA-2048", va='center', ha="left", bbox=face_comb)
ax3.text(-24,rsa2048_mark_decrypt, "303105")
ax3.set_ylabel('[ms]', fontsize=10)
ax3.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(keysizeticks)
plt.yticks(np.arange(0,330000,25000))
popt, pcov = curve_fit(lambda fx,a,b: a*fx**-b, keysizes, decrypt_times_ESP32)
x_linspace = np.linspace(min(keysizes), max(keysizes), 25000)
power_y = popt[0]*x_linspace**-popt[1]
plt.plot(x_linspace, power_y,linestyle=':')
plt.plot(155, rsa512_mark_decrypt, 'xr')
plt.plot(309, rsa1024_mark_decrypt, 'xr')
plt.plot(617, rsa2048_mark_decrypt, 'xr')

#              2 - ARDUINO MEGA PLOTS
#keysize vs keygen
rsa512_mark_MEGA_keygen = 75
fig4, ax4 = plt.subplots(1,figsize=(12,9))
ax4.plot(keysizes[0:13],keygen_time_MEGA)
ax4.axhline(y=rsa512_mark_MEGA_keygen, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax4.text(273,rsa512_mark_MEGA_keygen, "RSA-512", va='center', ha="left", bbox=face_comb)
ax4.text(24,rsa512_mark_MEGA_keygen, "75")
ax4.set_ylabel('[ms]', fontsize=10)
plt.xticks(np.arange(40,261,20))
ax4.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.plot(155, rsa512_mark_MEGA_keygen, 'xr')

#keysize vs encryption
rsa512_mark_MEGA_encrypt = 4101
fig5, ax5 = plt.subplots(1,figsize=(12,9))
ax5.plot(keysizes[0:13],encrypt_times_MEGA)
ax5.axhline(y=rsa512_mark_MEGA_encrypt, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax5.text(273,rsa512_mark_MEGA_encrypt, "RSA-512", va='center', ha="left", bbox=face_comb)
#ax5.text(24,rsa512_mark_MEGA_encrypt, "4101")
ax5.set_ylabel('[ms]', fontsize=10)
plt.xticks(np.arange(40,261,20))
ax5.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.plot(155, rsa512_mark_MEGA_encrypt, 'xr')

#keysize vs decryption
rsa512_mark_MEGA_decrypt = 331241
fig6, ax6 = plt.subplots(1,figsize=(12,9))
ax6.plot(keysizes[0:12],decrypt_times_MEGA)
ax6.axhline(y=rsa512_mark_MEGA_decrypt, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax6.text(252,rsa512_mark_MEGA_decrypt, "RSA-512", va='center', ha="left", bbox=face_comb)
ax6.text(18,rsa512_mark_MEGA_decrypt, "331241")
ax6.set_ylabel('[ms]', fontsize=10)
plt.xticks(np.arange(40,261,20))
ax6.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.plot(155, rsa512_mark_MEGA_decrypt, 'xr')

#              3 - ARDUINO UNO PLOTS
#keysize vs keygen
fig7, ax7 = plt.subplots(1,figsize=(12,9))
ax7.plot(keysizes[0:4],keygen_time_UNO)
ax7.set_ylabel('[ms]', fontsize=10)
plt.xticks(np.arange(40,121,20))
ax7.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')

#keysize vs encrypt

# - only one data point

#keysize vs decryption

# - failed instantly

#              4 - ESP8266 PLOTS
#keysize vs keygen
rsa512_mark_ESP8266_keygen = 5
rsa1024_mark_ESP8266_keygen = 10
fig8, ax8 = plt.subplots(1,figsize=(12,9))
ax8.plot(keysizes[0:16],keygen_time_ESP8266)
ax8.axhline(y=rsa512_mark_ESP8266_keygen, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax8.axhline(y=rsa1024_mark_ESP8266_keygen, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax8.text(325,rsa512_mark_ESP8266_keygen, "RSA-512", va='center', ha="left", bbox=face_comb)
ax8.text(325,rsa1024_mark_ESP8266_keygen, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax8.set_ylabel('[ms]', fontsize=10)
ax8.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(np.arange(40,321,20))
plt.plot(155, rsa512_mark_ESP8266_keygen, 'xr')
plt.plot(309, rsa1024_mark_ESP8266_keygen, 'xr')

#keysize vs encryption
rsa512_mark_ESP8266_encrypt = 179
rsa1024_mark_ESP8266_encrypt = 558
fig9, ax9 = plt.subplots(1,figsize=(12,9))
ax9.plot(keysizes[0:16],encrypt_times_ESP8266)
ax9.axhline(y=rsa512_mark_ESP8266_encrypt, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax9.axhline(y=rsa1024_mark_ESP8266_encrypt, color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax9.text(325,rsa512_mark_ESP8266_encrypt, "RSA-512", va='center', ha="left", bbox=face_comb)
ax9.text(325,rsa1024_mark_ESP8266_encrypt, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax9.set_ylabel('[ms]', fontsize=10)
ax9.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
plt.xticks(np.arange(40,321,20))
plt.plot(155, rsa512_mark_ESP8266_encrypt, 'xr')
plt.plot(309, rsa1024_mark_ESP8266_encrypt, 'xr')

#keysize vs decryption
fig10, ax10 = plt.subplots(1,figsize=(12,9))
ax10.plot(keysizes[0:5],decrypt_times_ESP8266)
ax10.set_ylabel('[ms]', fontsize=10)
ax10.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')


###### ALL DEVICES - keysize vs keygen
fig11,ax11 = plt.subplots(1,figsize=(12,9))
ax11.plot(keysizes,keygen_time_ESP32,label='ESP32') #ESP32
ax11.plot(keysizes[0:13],keygen_time_MEGA,label='MEGA') #MEGA
ax11.plot(keysizes[0:4],keygen_time_UNO,label='UNO') #UNO
ax11.plot(keysizes[0:16],keygen_time_ESP8266,label='ESP8266') #8266
ax11.axvline(x=155,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax11.axvline(x=309,ymin=0,ymax=0.55,color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax11.axvline(x=617,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-2048 (617 decimals)

ax11.text(162,25, "RSA-512", va='center', ha="left", bbox=face_comb)
ax11.text(316,25, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax11.text(565,25, "RSA-2048", va='center', ha="left", bbox=face_comb)

ax11.set_ylabel('[ms]', fontsize=10)
ax11.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
ax11.legend(loc='best')
plt.xticks(keysizeticks)
plt.yticks(np.arange(0,141,5))

###### ALL DEVICES - keysize vs encryption
fig12,ax12 = plt.subplots(1,figsize=(12,9))
ax12.plot(keysizes,encrypt_times_ESP32,label='ESP32') #ESP32
ax12.plot(keysizes[0:13],encrypt_times_MEGA,label='MEGA') #MEGA
#only one UNO datapoint, not plotted.
ax12.plot(keysizes[0:16],encrypt_times_ESP8266,label='ESP8266') #8266
ax12.axvline(x=155,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax12.axvline(x=309,ymin=0,ymax=0.55,color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax12.axvline(x=617,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-2048 (617 decimals)

ax12.text(162,2000, "RSA-512", va='center', ha="left", bbox=face_comb)
ax12.text(316,2000, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax12.text(565,2000, "RSA-2048", va='center', ha="left", bbox=face_comb)

ax12.set_ylabel('[ms]', fontsize=10)
ax12.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
ax12.legend(loc='best')
plt.xticks(keysizeticks)
plt.yticks(np.arange(0,10001,500))


###### ALL DEVICES - keysize vs decryption
fig13,ax13 = plt.subplots(1,figsize=(12,9))
ax13.plot(keysizes,decrypt_times_ESP32,label='ESP32') #ESP32
ax13.plot(keysizes[0:12],decrypt_times_MEGA,label='MEGA') #MEGA
#no UNO data points as it ran out of memory
ax13.plot(keysizes[0:5],decrypt_times_ESP8266,label='ESP8266') #8266
ax13.axvline(x=155,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-155 (RSA-512 bits)
ax13.axvline(x=309,ymin=0,ymax=0.55,color='gray', linestyle=':') #RSA-1024 (309 decimals)
ax13.axvline(x=617,ymin=0,ymax=0.55, color='gray', linestyle=':') #RSA-2048 (617 decimals)

ax13.text(162,125000, "RSA-512", va='center', ha="left", bbox=face_comb)
ax13.text(316,125000, "RSA-1024", va='center', ha="left", bbox=face_comb)
ax13.text(565,125000, "RSA-2048", va='center', ha="left", bbox=face_comb)

ax13.set_ylabel('[ms]', fontsize=10)
ax13.set_xlabel('[Public Key Size (# Decimals)]', fontsize='medium')
ax13.legend(loc='best')
plt.xticks(keysizeticks)
plt.yticks(np.arange(0,1240001,35000))


plt.show()
