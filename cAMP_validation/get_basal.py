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

def get_specie_index(header1, species_1):
    return [header1.index(specie) for specie in species_1]

for fname in fname_list:
    f = open(fname)
    header = f.readline().split()
    data = np.loadtxt(f)
    idx_567 = get_specie_index(header, species_567)
    idx_831 = get_specie_index(header, species_831)
    idx_845 = get_specie_index(header, species_845)
    for idx in idx_567:
        data567.append(data[:, idx])
    for idx in idx_831:
        data831.append(data[:, idx])
    for idx in idx_845:
        data845.append(data[:, idx])

print("845", np.array(data845).mean())    
print("831", np.array(data831).mean())
print("567", np.array(data567).mean())

    


