import matplotlib.pyplot as plt
import numpy as np
import glob 
fnames = glob.glob("model_4xHFS_3s_trial?_spine.txt")
datas = []
for f_name in fnames:
    f = open(f_name)
    header = f.readline().split()
    datas.append(np.loadtxt(f))

out = np.zeros_like(datas[0])

for data in datas:
    out += data
out = data/len(datas)

idx_ckp = header.index("CKp")
idx_ckpcam = header.index("CKpCaMCa4")

time = data[:, 0]

ckp = data[:, idx_ckp] + data[:, idx_ckpcam]
pkac = data[:, header.index("PKAc")]
plt.figure()
plt.plot(time, ckp)
plt.xlabel('time [s]')
plt.ylabel('Conc [nmol/l]')
plt.show()
