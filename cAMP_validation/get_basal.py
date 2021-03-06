import numpy as np
import glob

fname_list =  glob.glob("../model_start_trial*PSD.txt")

species_567 = ["GluR1_S567", "GluR1_S845_S567"]
species_831 = ["GluR1_S831", "GluR1_S845_S831"]
species_845 = ["GluR1_S845", "GluR1_S845_S831", "GluR1_S845_S567"]
out = 2000
data567 = []
data831 = []
data845 = []

def get_specie_index(header1, which_s):
    return [header1.index(specie) for specie in header1
            if which_s in specie]
mini = 100000
for i, fname in enumerate(fname_list):
    f = open(fname)
    header = f.readline().split()
    data = np.loadtxt(f)
    idx_567 = get_specie_index(header, "567")
    idx_831 = get_specie_index(header, "831")
    idx_845 = get_specie_index(header, "845")

    data567.append(data[:, idx_567].sum(axis=1))
    data831.append(data[:, idx_831].sum(axis=1))
    data845.append(data[:, idx_845].sum(axis=1))
    if mini > data.shape[0]:
        mini = data.shape[0]

new_data845 = [data[:mini] for data in data845]
new_data831 = [data[:mini] for data in data831]
new_data567 = [data[:mini] for data in data567]
print("845", np.array(new_data845).mean())    
print("831", np.array(new_data831).mean())
print("567", np.array(new_data567).mean())

    


