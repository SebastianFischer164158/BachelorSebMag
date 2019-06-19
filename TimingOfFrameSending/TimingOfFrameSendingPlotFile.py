import matplotlib.pyplot as plt
import numpy as np, scipy.stats as st
from scipy.optimize import curve_fit
plt.style.use("seaborn-darkgrid")
font = {'size'   : 15}

plt.rc('font', **font)
def mean_confidence_interval(data):
    conf = st.t.interval(0.95, len(data) - 1, loc=np.mean(data), scale=st.sem(data))
    return conf


five_seconds = np.array([142,142,147, 142, 141, 143, 139, 140, 140, 142])
ten_seconds = np.array([279, 275, 282, 280, 285, 276, 278, 285, 275, 274])
fifteen_seconds = np.array([421, 419, 429, 436, 405, 435, 423, 414, 418, 414])
twenty_seconds = np.array([547, 553, 591, 588, 588, 581, 577, 555, 561, 560])
twentyfive_seconds = np.array([727, 725, 712, 708, 731, 726, 724, 714, 735, 721])
thirty_seconds = np.array([873, 882, 872, 895, 871, 864, 893, 893, 855, 890])
#thirtyfive_seconds
#fourty_seconds
conf_array = []
dataarray = [five_seconds,ten_seconds,fifteen_seconds,twenty_seconds,twentyfive_seconds,thirty_seconds]
for item in dataarray:
    conf_array.append(mean_confidence_interval(item))

conf_range = []
for item in conf_array:
    conf_range.append(item[1] - item[0])

meanarray = []
for item in dataarray:
    meanarray.append(np.mean(item))

print(conf_array)
print(conf_range)
print(meanarray)


fig1, ax1 = plt.subplots(1,figsize=(12,9))
ax1.boxplot(dataarray,conf_intervals=[[conf_array[0][0],conf_array[0][1]],[conf_array[1][0],conf_array[1][1]],[conf_array[2][0],conf_array[2][1]],
                    [conf_array[3][0],conf_array[3][1]],[conf_array[4][0],conf_array[4][1]],[conf_array[5][0],conf_array[5][1]]])

ax1.scatter(np.full(10,1),dataarray[0],marker='x',s=25,alpha=0.6,label='5s - data points')
ax1.scatter(np.full(10,2),dataarray[1],marker='x',s=25,alpha=0.6,label='10s')
ax1.scatter(np.full(10,3),dataarray[2],marker='x',s=25,alpha=0.6,label='15s')
ax1.scatter(np.full(10,4),dataarray[3],marker='x',s=25,alpha=0.6,label='20s')
ax1.scatter(np.full(10,5),dataarray[4],marker='x',s=25,alpha=0.6,label='25s')
ax1.scatter(np.full(10,6),dataarray[5],marker='x',s=25,alpha=0.6,label='30s')
ax1.legend(loc='best',frameon=True,framealpha=0.5)

ax1.set_xticklabels(['5', '10', '15', '20','25','30'])
ax1.set_ylabel('Frames', fontsize=15)
ax1.set_xlabel('Time (s)', fontsize='medium')
plt.show()
