from __future__ import print_function, division

import matplotlib.pyplot as plt
import numpy as np
flist = [
    "model_start_100_trial0_dend_.txt",
    "model_start_300_trial0_dend_.txt",
    "model_start_1000_trial0_dend_.txt",
    "model_start_5000_trial0_dend_.txt",
    ]

if __name__ == "__main__":

    out = []
    for fname in flist:
        f = open(fname)
        header = f.readline().split()
        data = np.loadtxt(f)
        CKp = max(data[:, header.index('CKp')])
        out.append(CKp)
    out = np.array(out)
    out = out/out.max()
    plt.figure()
    plt.plot([100, 300, 1000, 5000], out)
    plt.xscale('log')
    plt.xlabel('CaMCa4 (nM)')
    plt.show()
