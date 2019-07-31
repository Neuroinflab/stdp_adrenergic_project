#!/usr/bin/env python
from __future__ import print_function, division, unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import glob

colors = ["gray",
          "maroon",
          "gold",
          "darkgreen",
          "forestgreen",
          "darkslategray",
          "darkturquoise",
          "dodgerblue",
          "midnightblue",
          "mediumblue",
          "indigo",
          "darkmagenta",
          "mediumvioletred"]

labels = [
    "DA",
    "ISO",
    "LFS",
    "HFS",
    "massed",
    "spaced",
    "ISO+LFS",
    "DA+LFS",
    "ISO+HFS"
]

filenames = [
    "../cAMP_validation/model_DA_bath_trial",
    "../cAMP_validation/model_ISO_bath_trial",
    "model_LFS_trial",
    "model_HFS_trial",
    "model_4xHFS_3s_trial",
    "model_4xHFS_80s_trial",
    "model_ISO_bath_LFS_trial",
    "model_DA_bath_LFS_trial",
    "model_ISO_bath_HFS_trial",
    ]

species = {"CaMKII": ["CKpCaMCa4", "CKpCaMCa4PP1", "CKp", "CKpPP1"],
           "Epac":   ["Epac1cAMP"],
           "PKA" : ["PKAc", "GluR1_S831_PKAc", "GluR1_PKAc", "GluR1_S567_PKAc",
                    "I1PKAc","PKAcISObAR","PKAcbAR",
                    "PKAcpISObAR","PKAcpbAR",
                    "PKAcppISObAR","PKAcppbAR",
                    "PKAcpppISObAR","PKAcpppbAR",
                    "PKAcNMDAR", "PKAc_PDE4_cAMP", "PKAcPDE4"],
           "Gi": ["Gibg"]
           }

evaluated_species = ["CaMKII", "PKA", "Epac", "Gi"]
endings = ["spine.txt", "dendrite.txt", "total.txt"]

if __name__ == "__main__":
    fig, ax = plt.subplots(len(endings),
                           len(evaluated_species),
                           figsize =(4*len(endings),
                                     4*(1+len(evaluated_species))))

    for i, filename in enumerate(filenames):
        for j, ending in enumerate(endings):
            pattern = "%s?_%s" % (filename, ending)
            fnames = glob.glob(pattern)
            for z, fname in enumerate(fnames):
                f = open(fname)
                header = f.readline().split()
                data = np.loadtxt(f)
                out = np.zeros((len(data), len(evaluated_species)+1))
                out[:, 0]  = data[:, 0]
                for k, specie in enumerate(header):
                    for idx, specie_set in enumerate(evaluated_species):
                        this_set = species[specie_set]
                        if specie in this_set:
                            out[:, idx+1] += data[:, k]

                for idx in range(len(evaluated_species)):
                    if idx == 0 and z == 0 and j == 0:
                        ax[j][idx].plot(out[:, 0], out[:, idx+1],
                                        color=colors[i], label=labels[i])
                    else:
                        ax[j][idx].plot(out[:, 0], out[:, idx+1],
                                        color=colors[i])

    for j, ending in enumerate(endings):
        ax[j][0].set_ylabel(ending[:-4])
    for idx, specie in enumerate(evaluated_species):
        ax[0][idx].set_title(specie)

    
    ax[0][3].legend()
    plt.show()
