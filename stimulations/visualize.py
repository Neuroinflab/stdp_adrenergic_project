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
    dir_names = glob.glob("?raham*")

    for dir_name in dir_names:
        if "zip" in dir_name:
            continue

        fnames = glob.glob("%s/*csv" % dir_name)

        for filename in fnames:
            if "neck" in filename:
                continue
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            head, res = read_in_file(filename)
            for i, column  in enumerate(res):
                if head[i] == "Compartment and Segment":
                    time = column
                else:
                    ax.plot(time, column, label=head[i])
                    ax.set_title(filename.split('/')[1])
                    lims = ax.get_xlim()
            ax.legend()
    plt.show()
    
