import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os.path
dt = 1

flist = [
    "graham_cai_4_spines_stdp_1500ms/cai_spine_head_10_dt_iclamp_1.60_nA_dur_3_ms.csv",
    "graham_cai_4_spines_stdp_1500ms/cai_spine_head_-20_dt_iclamp_1.60_nA_dur_3_ms.csv",
    "GrahamEtAl2014_0.75_NMDA/cai_spine_head_10_dt_iclamp_1.60_nA_dur_3_ms.csv",
    
    "GrahamEtAl2014_1.5_NMDA/cai_spine_head_-20_dt_iclamp_1.60_nA_dur_3_ms.csv",
    "GrahamEtAl2014_1.5_NMDA/cai_spine_head_-20_dt_iclamp_1.60_nA_dur_3_ms.csv",
]

labels = ["positve pairing",
          "negative pairing",
          "positive pairing + D1R antagonists",
          "negative pairing + DA bath",
          "negative pairing + ISO bath",
          ]

colors = ["k",
          "grey",
          "violet",
          "dodgerblue",
          "forestgreen",
          ]

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
#plt.rc('legend',fontsize=14)


def read_in_file(fname):
    try:
        f = open(fname)
    except IOError:
        sys.exit("IOError: no %s" % fname)
    out = []
    header = []

    for line in f:
        words = line.split(',')
        header += [words[0]]
        new_line = []
        for word in words[1:]:
            new_word = float(word)
            new_line.append(new_word)
        out.append(new_line)
    return header, np.array(out)



if __name__ == "__main__":

    f, ax = plt.subplots(1, 1)
    for j, filename in enumerate(flist):
        head, res = read_in_file(filename)
        for i, column  in enumerate(res):
            if head[i] == "Compartment and Segment":
                time = column
            elif head[i] == "PyramidalCell[0].shead[471].0.0":
                ax.plot(time, 1e6*column, label=labels[j], color=colors[j])
            print(head)
    ax.set_xlim([0, 500])
    ax.set_ylabel("Ca (nM)", fontsize=14)
    ax.set_xlabel("time (ms)", fontsize=14)
    ax.set_title("Calcium in the spine", fontsize=20)
    ax.legend()
    f.savefig("Calcium in the spine.svg",
              bbox_inches='tight',
              transparent=True,
              pad_inches=0.1)    
