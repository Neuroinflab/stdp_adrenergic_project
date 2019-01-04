#!/usr/bin/env python
# coding: utf-8
import h5py
import numpy as np
from lxml import etree
my_file = h5py.File('model_start.h5', 'r')
grid_list = np.array(my_file['model']['grid'])
#times, assuming that there is only one trial, trial0
times = np.array(my_file['trial0']['output']['__main__']['times'])
#time, voxel, specie
data = np.array(my_file['trial0']['output']['__main__']['population'])
subvolumes = list(my_file['model']['output']['__main__']['elements'])
species = list(my_file['model']['output']['__main__']['species'])
#1. calculate volume
regions = list(set([grid[15] for grid in grid_list]))
print(list(my_file['model'].keys()))
xml_input = my_file['model']['serialized_config'][0]
print(xml_input)
