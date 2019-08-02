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
    #"DA",
    #"ISO",
    "LFS",
    #"HFS",
    #"massed",
    #"spaced",
    #"ISO+LFS",
    #"DA+LFS",
    #"ISO+HFS"
]

filenames = [
    #"../cAMP_validation/model_DA_bath_trial",
    #"../cAMP_validation/model_ISO_bath_trial",
    "model_LFS_trial",
    #"model_HFS_trial",
    #"model_4xHFS_3s_trial",
    #"model_4xHFS_80s_trial",
    #"model_ISO_bath_LFS_trial",
    #"model_DA_bath_LFS_trial",
    #"model_ISO_bath_HFS_trial",
    ]

species = {"CaMKII": ["CKpCaMCa4", "CKp", ],
           "Epac":   ["Epac1cAMP"],
           "PKA" : ["PKAc", "GluR1_S831_PKAc", "GluR1_PKAc", "GluR1_S567_PKAc",
                    "I1PKAc","PKAcISObAR","PKAcbAR",
                    "PKAcpISObAR","PKAcpbAR",
                    "PKAcppISObAR","PKAcppbAR",
                    "PKAcpppISObAR","PKAcpppbAR",
                    "PKAcNMDAR", "PKAc_PDE4_cAMP", "PKAcPDE4"],
           "Gi": ["Gibg"],
           "PP1": ["CKpCaMCa4PP1", "CKpPP1", "GluR1_S845_PP1",
                   "GluR1_S567_PP1", "GluR1_S831_PP1",
                   "GluR1_S845_S831_PP1", "GluR1_S845_S567_PP1",
                   "GluR1_S845_S831_PP1_2", "GluR1_S845_S567_PP1_2",
                   "PP1", "PP1pNMDAR"],
           "PP2B":["PP2BCaMCa4", "GluR1_S845_PP2B",
                   "GluR1_S845_S831_PP2B", "GluR1_S845_S567_PP2B",
                   "Ip35PP1PP2BCaMCa4", "Ip35PP2BCaMCa4",
                   "PP2BpNMDAR"],
           "S845": ["GluR1_S845", "GluR1_S845_S831", "GluR1_S845_S567"],
           "S831": ["GluR1_S831", "GluR1_S845_S831"],
           "S567": ["GluR1_S567",  "GluR1_S845_S567"],
           "pNMDAR": ["pNMDAR"],

           }

evaluated_species = ["CaMKII", "PKA", "Epac", "Gi", "PP1",
                     "PP2B"]
endings = ["spine.txt", "dendrite.txt", "total.txt"]

if __name__ == "__main__":
    fig, ax = plt.subplots(len(endings),
                           len(evaluated_species),
                           figsize =(5*len(endings),
                                     5*(1+len(evaluated_species))))

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
                for idx, specie_set in enumerate(evaluated_species):
                    this_set = species[specie_set]
                    for specie in this_set:
                        k = header.index(specie)
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

    
    fig.legend(loc=7)
    plt.show()
