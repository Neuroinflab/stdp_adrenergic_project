import numpy as np
import glob

fname_list = glob.glob("model_DA_bath_20_uM_trial*PSD.txt")+ glob.glob("model_DA_bath_trial*PSD.txt")+ glob.glob("model_ISO_bath_trial*PSD.txt")

species_567 = ["GluR1_S567", "GluR1_S845_567"]
species_831 = ["GluR1_S831", "GluR1_S845_831"]
out = 2000
data567 = []
data831 = []

for fname in fname_list:
    f = open(fname)
    header = f.readline().split()
    data = np.loadtxt(f)
    idx_567 = [header.index("GluR1_S567"), header.index("GluR1_S845_S567")]
    idx_831 = [header.index("GluR1_S831"), header.index("GluR1_S845_S831")]
    data831.append(data[:2000, idx_831[0]] +data[:2000, idx_831[1]])
    data567.append(data[:2000, idx_567[0]] +data[:2000, idx_567[1]])
    
print("831", np.array(data831).mean())
print("567", np.array(data567).mean())

    


