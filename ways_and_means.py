from __future__ import division, print_function
import numpy as np
import sys
import argparse
parser = argparse.ArgumentParser(description='Print out averages')
parser.add_argument('files', nargs='+', help='Conc filenames')
parser.add_argument('--species', dest="species", default='cAMP,Ca',
                    help='Specie list, default cAMP,Ca')


if __name__ == "__main__":
    args = parser.parse_args()
    species = args.species.split(",")
    for fname in args.files:
        f = open(fname)
        header = f.readline().split()
        data = np.loadtxt(f)
        for specie in species:
            try:
                idx = header.index(specie)
            except ValueError:
                print("No %s in %s" % (specie, fname))
                continue
            mean = data[:, idx].mean()
            std =  np.sqrt(data[:, idx].var())
            out = "%s, mean: %f, std: %f" % (specie, mean, std)
            print(out)
