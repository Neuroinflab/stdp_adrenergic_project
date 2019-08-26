from __future__ import division, print_function
import glob
import numpy as np
import matplotlib.pyplot as plt
labels = ['trial 0', 'trial 1', 'trial 2', 'trial 3']

parser = argparse.ArgumentParser(description='Make average specie concentration plots')

parser.add_argument('files', nargs='+', help='Conc filenamses')
parser.add_argument('--species', dest="species", default='Epac1cAMP',
                    help='Specie list, default Epac1cAMP')

def read_in_species(species):
    old_species = species.split(',')
    new_species = []
    for specie in old_species:
        new_species.append(specie.strip())
    return new_species

def get_basal(filename):
    region = filename.split("_")[-1].split(".")[0]
    print(region)
    trial = filename.split("trial")[-1].split("_")[0]
    print(trial)
    basal_fname = "model_start_trial%d_%s.txt" % (trial, region)
    f = open(filename)
    header = f.readline().split()
    data = np.loadtxt(f)
    return data, header



if __name__ == '__main__':
    args = parser.parse_args()
    species = read_in_species(args.species)
    data = []
    times = []
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    basal = []
    for fname in args.files:
        print(fname)
        try:
            f = open(fname)
        except IOError:
            print("Could not find %s" % fname)
        header = f.readline().split()
        temp_data = np.loadtxt(f)
        basal_header, basal_data = get_basal(filename)
        times.append(temp_data[:, header.index('time')])
        data.append(temp_data[:, header.index(specie_name)])
        basal.append(basal_data[:, basal_header.index(specie_name)])


    data_len = max([len(d) for d in data])
    averaged_data = np.zeros((data_len, 1))
    max_time = np.concatenate(times).max()
    dt = times[0][1]-times[0][0]
    averaged_time = np.linspace(0, max_time, data_len)
    mean = []
    for dat in data:
        mean.append(dat[:int(300000/dt)].mean())
        for i, d in enumerate(data):
            averaged_data[:len(d), 0] += d
            ax.plot(times[i], (d-mean[i])/mean[i], label=labels[i])
        averaged_data = averaged_data/len(data)
        averaged_mean = averaged_data.mean()

        ax.plot(averaged_time, (averaged_data-averaged_mean)/averaged_mean, label="Averaged", linewidth=3)
        if j:
            ax.set_title('ISO bath: Epac-bound cAMP')
        else:
            ax.set_title('DA bath: Epac-bound cAMP')       
        ax.legend()
    plt.show()




