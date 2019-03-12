import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

keysizes_ESP32 = np.arange(40,621,20)
encrypt_times_ESP32 = np.array([11, 19, 34, 47, 57, 67, 101, 122,
                          135, 152, 164, 180, 199, 214, 304,
                          348, 361, 390, 401, 431, 448,
                          480, 512, 529, 550, 575, 596, 612, 635, 657])

decryption_times_ESP32 = np.array([160, 447, 1188, 2254, 3287, 4717, 8523,
                                   12153, 14976, 18679, 22360, 27233, 33423,
                                   38386, 61677, 74499, 84099, 94113, 103109,
                                   118499, 131548, 148389, 164413, 178871, 197647,
                                   214849, 235389, 251535, 276178, 294126])
                                   
keygen_time_ESP32 = np.array([2,3,3,4,4,4,6,6,6,5,6,6,6,7,10,11,12,12,12,13,13,13,13,15,15,15,15,15,16,17])
print(len(keygen_time_ESP32))
#print(len(decryption_times_ESP32))

sns.set()

plt.plot(encrypt_times_ESP32,keysizes_ESP32)
plt.plot(keysizes_ESP32,decryption_times_ESP32)
plt.plot(keysizes_ESP32,keygen_time_ESP32)
plt.show()
