from __future__ import division, print_function
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Print out averages')
parser.add_argument('files', nargs='+', help='Conc filenames')
parser.add_argument('--species', dest="species", default='cAMP,Ca',
                    help='Specie list, default cAMP,Ca')

def read_in_species(species):
    old_species = species.split(',')
    new_species = []
    for specie in old_species:
        new_species.append(specie.strip())
    return new_species

if __name__ == "__main__":
    args = parser.parse_args()
    species = read_in_species(args.species)
    
    for fname in args.files:
        print(fname)
        try:
            f = open(fname)
        except IOError:
            print("Could not find %s" % fname)
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
