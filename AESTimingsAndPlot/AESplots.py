import matplotlib.pyplot as plt
import numpy as np, scipy.stats as st
from scipy.optimize import curve_fit
plt.style.use("seaborn-darkgrid")
import itertools
font = {'size'   : 15}

plt.rc('font', **font)
def mean_confidence_interval(data):
    conf = st.t.interval(0.95, len(data) - 1, loc=np.mean(data), scale=st.sem(data))
    return conf

#250 data points each
AES_encrypt_times_ESP32 = np.array([301,294,294,294,302,294,302,294,294,301,294,302,294,295,302,294,302,294,294,302,
                                    294,302,294,294,302,294,301,294,294,302,294,302,294,294,302,294,301,294,294,302,
                                    294,302,294,294,302,295,302,294,294,301,294,301,294,295,302,294,302,294,294,302,
                                    294,302,294,294,294,294,302,295,294,294,294,302,294,294,294,294,302,294,294,294,
                                    294,302,294,294,294,294,302,294,294,294,294,301,294,294,294,294,301,294,294,294,
                                    294,302,294,294,294,294,302,294,294,294,294,301,294,294,294,294,301,294,294,294,
                                    294,302,294,301,294,294,301,294,301,294,295,302,294,302,294,294,302,294,302,294,
                                    294,302,294,302,294,294,302,294,302,294,294,301,294,302,294,294,302,294,302,294,
                                    294,301,294,301,294,294,302,294,302,294,294,302,294,301,294,294,302,294,302,294,
                                    294,294,294,301,294,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    294,294,294,302,295,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    302,295,294,302,294,302,295,294,302,294])
AES_encrypt_times_ESP8266 = np.array([414,414,414,414,414,414,414,413,413,414,414,414,414,414,414,414,414,413,413,414,
                                      414,414,414,414,414,414,414,414,414,414,414,414,414,413,413,414,414,414,414,414,
                                      414,414,414,413,413,414,414,414,414,414,414,414,414,413,413,414,414,414,414,414,
                                      414,414,414,413,413,414,414,414,414,414,414,420,413,414,414,414,414,414,414,414,
                                      414,414,413,414,414,414,414,414,414,414,414,414,413,414,414,414,414,414,414,414,
                                      414,414,413,414,414,414,414,414,414,414,414,414,413,414,414,414,414,414,414,414,
                                      414,414,413,414,414,414,414,414,414,414,414,414,413,414,414,414,414,414,414,414,
                                      414,414,413,414,414,414,414,414,414,414,414,414,414,414,414,414,414,414,414,414,
                                      414,413,414,414,414,414,414,414,414,414,414,413,414,414,414,414,414,414,414,414,
                                      414,413,414,414,414,414,414,414,414,414,414,413,414,414,420,414,414,414,414,413,
                                      413,414,414,414,414,414,414,414,414,413,413,414,414,414,414,414,414,414,414,413,
                                      413,414,414,414,414,414,414,414,414,413,413,414,414,414,414,414,414,414,414,413,
                                      413,414,414,414,414,414,414,414,414,413])
AES_encrypt_times_MEGA = np.array([9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9252,9256,9256,9256,9256,9256,9260,
                                   9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9252,9256,9256,9264,9256,9256,9252,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9264,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9252,9256,9256,9256,9256,9256,9256,
                                   9264,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9252,9256,9256,9256,9260,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9264,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9252,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9260,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9252,9256,9256,9256,9256,9256,9252,9256,9256,9256,9256,9264,9256,9256,9256,9256,
                                   9256,9256,9256,9256,9256,9256,9256,9256,9260,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,9256,
                                   9256,9252,9256,9256,9256,9256,9256,9252,9256,9256])

AES_encrypt_times_MEGA = np.divide(AES_encrypt_times_MEGA,1000) #vi converter til miliseconds
AES_encrypt_times_ESP8266 = np.divide(AES_encrypt_times_ESP8266,1000)
AES_encrypt_times_ESP32 = np.divide(AES_encrypt_times_ESP32,1000)

AES_decrypt_times_ESP32 = np.array([294,294,294,294,302,294,302,294,294,301,294,302,294,295,302,294,302,294,294,302,
                                    294,302,294,294,302,294,301,294,294,302,294,302,294,294,302,294,301,294,294,302,
                                    294,302,294,294,302,295,302,294,294,301,294,301,294,295,302,294,302,294,294,302,
                                    294,302,294,294,294,294,302,295,294,294,294,302,294,294,294,294,302,294,294,294,
                                    294,302,294,294,294,294,302,294,294,294,294,301,294,294,294,294,301,294,294,294,
                                    294,302,294,294,294,294,302,294,294,294,294,301,294,294,294,294,301,294,294,294,
                                    294,302,294,301,294,294,301,294,301,294,295,302,294,302,294,294,302,294,302,294,
                                    294,302,294,302,294,294,302,294,302,294,294,301,294,302,294,294,302,294,302,294,
                                    294,301,294,301,294,294,302,294,302,294,294,302,294,301,294,294,302,294,302,294,
                                    294,294,294,301,294,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    294,294,294,302,295,294,294,294,302,294,294,294,294,302,294,294,294,294,302,294,
                                    302,295,294,302,294,302,295,294,302,294])
AES_decrypt_times_ESP8266 = np.array([420,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,421,419,
                                      419,419,419,425,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,425,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,
                                      419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419,419])
AES_decrypt_times_MEGA = np.array([9352,9352,9348,9348,9348,9348,9348,9348,9348,9348,9348,9348,9348,9356,9348,9348,9348,9348,9352,9348,
                                   9348,9356,9348,9352,9348,9348,9356,9348,9352,9352,9348,9348,9348,9348,9356,9348,9348,9348,9348,9356,
                                   9348,9348,9348,9348,9348,9348,9348,9352,9348,9348,9348,9348,9348,9348,9348,9348,9348,9348,9348,9348,
                                   9356,9348,9348,9348,9348,9352,9352,9348,9356,9348,9348,9352,9348,9356,9348,9348,9352,9348,9348,9348,
                                   9348,9356,9348,9348,9348,9348,9356,9348,9348,9348,9348,9348,9348,9348,9352,9348,9348,9348,9348,9348,
                                   9348,9348,9356,9352,9348,9348,9348,9352,9352,9348,9348,9348,9348,9348,9348,9356,9348,9348,9348,9348,
                                   9356,9348,9348,9348,9348,9348,9348,9348,9356,9348,9348,9348,9348,9348,9348,9352,9348,9348,9348,9348,
                                   9352,9352,9348,9348,9348,9352,9348,9348,9348,9352,9348,9348,9348,9348,9352,9348,9348,9348,9348,9348,
                                   9348,9348,9356,9348,9348,9348,9348,9356,9348,9348,9348,9348,9352,9348,9348,9356,9348,9352,9348,9348,
                                   9348,9348,9352,9356,9348,9348,9348,9348,9356,9348,9348,9348,9348,9348,9348,9348,9352,9348,9348,9348,
                                   9348,9352,9348,9348,9348,9348,9348,9348,9348,9356,9348,9348,9348,9348,9352,9348,9348,9348,9348,9352,
                                   9352,9348,9356,9348,9348,9352,9348,9348,9348,9348,9356,9348,9348,9348,9348,9356,9348,9348,9348,9348,
                                   9348,9348,9348,9352,9348,9348,9348,9348,9352,9348])

AES_decrypt_times_MEGA = np.divide(AES_decrypt_times_MEGA,1000)
AES_decrypt_times_ESP8266 = np.divide(AES_decrypt_times_ESP8266,1000)
AES_decrypt_times_ESP32 = np.divide(AES_decrypt_times_ESP32,1000)



data_array_encrypt = [AES_encrypt_times_ESP32,AES_encrypt_times_ESP8266,AES_encrypt_times_MEGA]
data_array_decrypt = [AES_decrypt_times_ESP32,AES_decrypt_times_ESP8266,AES_decrypt_times_MEGA]

conf_array_encrypt = [mean_confidence_interval(item) for item in data_array_encrypt]
conf_array_decrypt = [mean_confidence_interval(item) for item in data_array_decrypt]

print("Confidence interval array, encryption: \n",conf_array_encrypt)
print("Confidence interval array, decryption: \n",conf_array_decrypt)

conf_range_encrypt = [confrange[1] - confrange[0] for confrange in conf_array_encrypt]
conf_range_decrypt = [confrange[1] - confrange[0] for confrange in conf_array_decrypt]

print(conf_range_encrypt)
print(conf_range_decrypt)

meanarray_encrypt = [np.mean(x) for x in data_array_encrypt]
meanarray_decrypt = [np.mean(x) for x in data_array_decrypt]

print(meanarray_encrypt)
print(meanarray_decrypt)
xticks_array = ['ESP32','ESP8266','MEGA']
#ALL DEVICES ENCRYPTION & DECYPTION

fig1, ax1 = plt.subplots(1,figsize=(12,9))
ax1.scatter(np.ones(250),data_array_encrypt[0],marker='x',s=25,alpha=0.6,label=xticks_array[0])
ax1.scatter(np.full(250,2),data_array_encrypt[1],marker='x',s=25,alpha=0.6,label=xticks_array[1])
ax1.scatter(np.full(250,3),data_array_encrypt[2],marker='x',s=25,alpha=0.6,label=xticks_array[2])
ax1.legend(loc='best',frameon=True,framealpha=0.5)
ax1.boxplot(data_array_encrypt)
ax1.set_xticklabels(xticks_array)
plt.title("ALL DEVICES AES ENCRYPTION")
ax1.set_ylabel('Time (ms)', fontsize=15)
ax1.set_xlabel('Devices', fontsize='medium')

fig5, ax5 = plt.subplots(1,figsize=(12,9))
ax5.scatter(np.ones(250),data_array_decrypt[0],marker='x',s=25,alpha=0.6,label=xticks_array[0])
ax5.scatter(np.full(250,2),data_array_decrypt[1],marker='x',s=25,alpha=0.6,label=xticks_array[1])
ax5.scatter(np.full(250,3),data_array_decrypt[2],marker='x',s=25,alpha=0.6,label=xticks_array[2])
ax5.legend(loc='best',frameon=True,framealpha=0.5)
ax5.boxplot(data_array_decrypt)
ax5.set_xticklabels(xticks_array)
plt.title("ALL DEVICES AES DECRYPTION")
ax5.set_ylabel('Time (ms)', fontsize=15)
ax5.set_xlabel('Devices', fontsize='medium')

#ESP32
fig2, ax2 = plt.subplots(1,figsize=(12,9))
ax2.scatter(np.ones(250),data_array_encrypt[0],marker='x',s=25,alpha=0.6,label=xticks_array[0])
ax2.legend(loc='best',frameon=True,framealpha=0.5)
ax2.boxplot(data_array_encrypt[0])
ax2.set_xticklabels(xticks_array[0])
plt.title("ESP32 AES ENCRYPTION")
ax2.set_ylabel('Time (ms)', fontsize=15)
ax2.set_xlabel('Devices', fontsize='medium')

fig6, ax6 = plt.subplots(1,figsize=(12,9))
ax6.scatter(np.ones(250),data_array_decrypt[0],marker='x',s=25,alpha=0.6,label=xticks_array[0])
ax6.legend(loc='best',frameon=True,framealpha=0.5)
ax6.boxplot(data_array_decrypt[0])
ax6.set_xticklabels(xticks_array[0])
plt.title("ESP32 AES DECRYPTION")
ax6.set_ylabel('Time (ms)', fontsize=15)
ax6.set_xlabel('Devices', fontsize='medium')

#ESP8266
fig3, ax3 = plt.subplots(1,figsize=(12,9))
ax3.scatter(np.ones(250),data_array_encrypt[1],marker='x',s=25,alpha=0.6,label=xticks_array[1])
ax3.legend(loc='best',frameon=True,framealpha=0.5)
ax3.boxplot(data_array_encrypt[1])
ax3.set_xticklabels(xticks_array[1])
plt.title("ESP8266 AES ENCRYPTION")
ax3.set_ylabel('Time (ms)', fontsize=15)
ax3.set_xlabel('Devices', fontsize='medium')

fig7, ax7 = plt.subplots(1,figsize=(12,9))
ax7.scatter(np.ones(250),data_array_decrypt[1],marker='x',s=25,alpha=0.6,label=xticks_array[1])
ax7.legend(loc='best',frameon=True,framealpha=0.5)
ax7.boxplot(data_array_decrypt[1])
ax7.set_xticklabels(xticks_array[1])
plt.title("ESP8266 AES DECRYPTION")
ax7.set_ylabel('Time (ms)', fontsize=15)
ax7.set_xlabel('Devices', fontsize='medium')


#MEGA
fig4, ax4 = plt.subplots(1,figsize=(12,9))
ax4.scatter(np.ones(250),data_array_encrypt[2],marker='x',s=25,alpha=0.6,label=xticks_array[2])
ax4.legend(loc='best',frameon=True,framealpha=0.5)
ax4.boxplot(data_array_encrypt[2])
ax4.set_xticklabels(xticks_array[2])
plt.title("MEGA AES ENCRYPTION")
ax4.set_ylabel('Time (ms)', fontsize=15)
ax4.set_xlabel('Devices', fontsize='medium')

fig8, ax8 = plt.subplots(1,figsize=(12,9))
ax8.scatter(np.ones(250),data_array_decrypt[2],marker='x',s=25,alpha=0.6,label=xticks_array[2])
ax8.legend(loc='best',frameon=True,framealpha=0.5)
ax8.boxplot(data_array_decrypt[2])
ax8.set_xticklabels(xticks_array[2])
plt.title("MEGA AES DECRYPTION")
ax8.set_ylabel('Time (ms)', fontsize=15)
ax8.set_xlabel('Devices', fontsize='medium')

plt.show()
