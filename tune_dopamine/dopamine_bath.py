from __future__ import division, print_function
import glob
import numpy as np
import matplotlib.pyplot as plt
labels = ['trial 0', 'trial 1', 'trial 2']
stim_time = 50000
specie_name = "Epac1cAMP"
file_list = glob.glob("*dopamin*total.txt")

data = []
times = []
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for i, fname in enumerate(file_list):
    ff = open(fname)
    header = ff.readline().split(' ')
    temp_data = np.loadtxt(ff)
    times.append(temp_data[:, header.index('time')])
    data.append(temp_data[:, header.index(specie_name)])
                 
data_len = max([len(d) for d in data])
averaged_data = np.zeros((data_len, 1))
max_time = np.concatenate(times).max()
averaged_time = np.linspace(0, max_time, data_len)

for i, d in enumerate(data):
    averaged_data[:len(d), 0] += d
    ax.plot(times[i], d, label=labels[i])
averaged_data = averaged_data/len(data)
ax.plot(averaged_time, averaged_data, label="Averaged", linewidth=3)
ax.set_title('Epac-bound cAMP')
ax.legend()
plt.show()




