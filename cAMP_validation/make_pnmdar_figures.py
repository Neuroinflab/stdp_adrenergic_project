from __future__ import print_function, division, unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import glob
fnames_DA_pnmdar = glob.glob("model_DA_bath_20_uM_trial?_PSD.txt")
fnames_ISO_pnmdar = glob.glob("model_ISO_bath_trial?_PSD.txt")
fnames_SCH_pnmdar = glob.glob("model_SCH_23390_bath_trial?_PSD.txt")
fnames_control_pnmdar = glob.glob("../model_start_trial?_PSD.txt")

fnames_DA_epacs = glob.glob("model_DA_bath_trial?_total.txt")
fnames_ISO_epacs = glob.glob("model_ISO_bath_trial?_total.txt")
fnames_control_epacs = glob.glob("../model_start_trial?_total.txt")

labels = [u"Dopamine 20 μM", u"Isoproterenol 1 μM", "D1R antagonist", "control"]

list1 = [fnames_DA_epacs, fnames_ISO_epacs]

list2 = [fnames_DA_pnmdar, fnames_ISO_pnmdar,fnames_SCH_pnmdar ]
lists = [list1, list2]
titles = ["cAMP activity",
          "NMDAR phosphorylation"]

fnames = ["cAMP_activity.svg",
          "NMDAR_phosphorylation.svg"]

colors = ["dodgerblue", "forestgreen","violet", "k"]
specie = ["Epac1cAMP", "pNMDAR"]

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
#plt.rc('legend',fontsize=14)

def read_in_data(f_list, specie):
    out = []
    times = []
    for f_name in f_list:
        f = open(f_name)
        header = f.readline().split()
        data = np.loadtxt(f)
        times.append(data[:,0])
        out.append(data[:, header.index(specie)])

    return times, out


def make_average(arrs, control):
    lens = np.array([len(arr) for arr in arrs])
    if np.all(lens == lens[0]):
        out = np.array(arrs)
    else:
        min_len = min(lens)
        out = np.ndarray((len(arrs), min_len))
        for i, arr in enumerate(arrs):
            out[i] = arr[:min_len]
        
    if control:
        print(out[:,:1500].mean())
        out = (out - out[:, :1500].mean())/out[:,:1500].mean()
    mean = out.mean(axis=0)
    mean_var = np.sqrt(out.var(axis=0)/len(arrs))
    return mean, mean_var


def make_time(arrs):
    lens = np.array([len(arr) for arr in arrs])
    if np.all(lens == lens[0]):
        return arrs[0]
    argmin = np.argmin(lens)

    try: 
        return arrs[argmin]
    except:
        return arrs[argmin[0]]


def make_data(f_list, specie, control=False):
    times, outs = read_in_data(f_list, specie)
    time = make_time(times)
    outs_mean, outs_error = make_average(outs, control)
    return time, outs_mean, outs_error


if __name__ == '__main__':

    for i, par in enumerate(lists):
        title = titles[i]
        fig, ax = plt.subplots(1, 1)
        for j, flist in enumerate(par):
            time, mean, error = make_data(flist, specie[i], control=not i)
            ax.plot(time/1000, mean,
                    color=colors[j], label=labels[j])
            if i:
                ax.plot(time/1000, 800*np.ones_like(time), "k")
        ax.legend(loc=3)
        ax.set_xlabel("time (s)", fontsize=14)
        ax.set_ylabel("% change", fontsize=14)
        ax.set_title(titles[i], fontsize=20)
        fig.savefig(fnames[i], bbox_inches='tight',
                    transparent=True, pad_inches=0.1)
        
        
