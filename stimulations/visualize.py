import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os.path
dt = 1

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
    dir_name = "graham_cai_4_spines_stdp_1500ms/"
    fnames = glob.glob("%s*csv" % dir_name)
    
    for filename in fnames:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        head, res = read_in_file(filename)
        time = np.arange(0, (res.shape[1])*dt, dt)
        for i, column  in enumerate(res):
            if "head" in head[i]:
                ax.plot(time, column, label=head[i])
                ax.set_title(filename)
        ax.legend()
    plt.show()
    
