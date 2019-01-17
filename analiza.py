#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function, division
import h5py
import numpy as np
from lxml import etree
import sys

spine = ['PSD', 'head', 'neck']

def nano_molarity(N, V):
    return 10*N/V/6.02214076

def pico_sd(N, S):
    return 10*N/S/6.02214076

def get_all_species(root):
    all_species = []
    for son in root:
        if son.tag.endswith('ReactionScheme'):
            for grandson in son:
                if grandson.tag.endswith('Specie'):
                    all_species.append(grandson.get('id'))
    return list(set(all_species))

def get_all_anchored_species(root):
    all_species = []
    for son in root:
        if son.tag.endswith('ReactionScheme'):
            for grandson in son:
                if grandson.tag.endswith('Specie'):
                    if not float(grandson.get("kdiff")):
                        all_species.append(grandson.get('id'))
    return list(set(all_species))


def get_all_submembrane_species(my_file):
    root = etree.fromstring(my_file['model']['serialized_config'][0])
    all_anchored_species = get_all_anchored_species(root)
    anchored = []
    for son in root:
        if son.tag.endswith('InitialConditions'):
            for grandson in son:
                if grandson.tag.endswith("SurfaceDensitySet"):
                    for grandgrandson in grandson:
                        name = grandgrandson.get("specieID")
                        if  name in all_anchored_species:
                            anchored.append(name)
    return list(set(anchored))
                    
def region_volumes(my_file):
    grid_list = np.array(my_file['model']['grid'])
    regions =  get_regions(my_file)
    volumes = {}
    for region in regions:
        volumes[region] = 0
    for cell in grid_list:
        volumes[cell[15]] += float(cell[12])
    return volumes

def sum_volume(my_file, region_list):
    grid_list = np.array(my_file['model']['grid'])
    vol_sum = 0
    volumes = region_volumes(my_file)
    for region in region_list:
        if region in volumes:
            vol_sum += volumes[region]
    return vol_sum

def sum_indices(my_file, region_list):
    reg_indices = get_region_indices(my_file)
    sum_indices = []
    for region in region_list:
        if region in reg_indices:
            sum_indices += reg_indices[region]
    return sum_indices

    
def region_surface(grid_list, direction=0):
    submembrane_regions = []
    submembrane_regions_dict = {}
    for i, cell in enumerate(grid_list):
        if cell[17] == b'submembrane':
            if cell[15] not in submembrane_regions:
                submembrane_regions.append(cell[15])
                submembrane_regions_dict[cell[15]] = []
            submembrane_regions_dict[cell[15]].append(i)
    surface = {}
    for key in submembrane_regions_dict:
        surface[key] = 0
        for cell_idx in submembrane_regions_dict[key]:
            if direction == 0:
                depth = grid_list[cell_idx][13]
                width = abs(grid_list[cell_idx][0]-grid_list[cell_idx][3])
                surface[key] += depth*width
            else:
                print('Unimplemented direction', direction)
    return surface

def get_region_indices(my_file):
    region_ind = {}
    for idx, cell in enumerate(grid_list):
        if cell[15] not in region_ind:
            region_ind[cell[15]] = []
        region_ind[cell[15]].append(idx)
    return region_ind

def get_regions(my_file):
    grid_list = np.array(my_file['model']['grid'])
    return sorted(list(set([grid[15] for grid in grid_list])))

def get_concentrations_region_list(my_file, my_list):
    times = np.array(my_file['trial0']['output']['__main__']['times'])
    grid_list = np.array(my_file['model']['grid'])
    data = np.array(my_file['trial0']['output']['__main__']['population'])
    species = list(my_file['model']['output']['__main__']['species'])
    idxs = sum_indices(my_file, my_list)
    vol = sum_volume(my_file, my_list)
    numbers = data[:, idxs, :].sum(axis=1)
    return nano_molarity(numbers, vol)
    
def get_concentrations(my_file):
    times = np.array(my_file['trial0']['output']['__main__']['times'])
    grid_list = np.array(my_file['model']['grid'])
    data = np.array(my_file['trial0']['output']['__main__']['population'])
    species = list(my_file['model']['output']['__main__']['species'])
    regions = get_regions(my_file)
    
    submembrane_species = get_all_submembrane_species(my_file)
    volume_dict = region_volumes(my_file)
    surface_dict = region_surface(grid_list)
    concentrations = np.zeros((len(times), len(regions), len(species)))
    numbers =  np.zeros((len(times), len(regions), len(species)))
    region_indices = get_region_indices(grid_list)
    for i, reg in enumerate(regions):
        # get numbers
        numbers[:, i, :] = data[:, region_indices[reg], :].sum(axis=1)
        if reg in surface_dict:
            for j, specie in enumerate(species):
                if specie in submembrane_species:
                    concentrations[:, i, j] = pico_sd(numbers[:, i, j],
                                                      surface_dict[reg])
                else:
                    concentrations[:, i, j] = nano_molarity(numbers[:, i, j],
                                                            volume_dict[reg])
        else:
            concentrations[:, i, :] = nano_molarity(numbers[:, i, :],
                                                    volume_dict[reg])
    print(volume_dict)
    return concentrations


def save_single_file(times, concentrations, species, fname):
    header = 'time'
    for specie in species:
        header += ' ' + specie
    what_to_save = np.zeros((len(times), len(species) + 1))
    what_to_save[:, 0] = times
    what_to_save[:, 1:] = concentrations
    camp_idx = species.index('cAMP')
    print(fname, concentrations[:, camp_idx].mean(), concentrations[:, camp_idx].var()**0.5)
    np.savetxt(fname, what_to_save, header=header, comments='')
    
def save_concentrations(my_file, fname_base, my_list=None):
    times = np.array(my_file['trial0']['output']['__main__']['times'])
    species = list(my_file['model']['output']['__main__']['species'])
    regions = get_regions(my_file)
    concentrations = get_concentrations(my_file)

    for i, region in enumerate(regions):
        fname = '%s_%s.txt' % (fname_base, region)
        save_single_file(times, concentrations[:, i, :], species, fname)
    totals = get_concentrations_region_list(my_file, regions)
    save_single_file(times, totals, species, '%s_%s.txt' % (fname_base, 'total'))
    spine = get_concentrations_region_list(my_file, ['PSD', 'head', 'neck'])
    save_single_file(times, spine, species, '%s_%s.txt' % (fname_base, 'spine'))
    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('No filename provided')
    fname = sys.argv[1]
    my_file = h5py.File(fname, 'r')
    grid_list = np.array(my_file['model']['grid'])
    #times, assuming that there is only one trial, trial0
    times = np.array(my_file['trial0']['output']['__main__']['times'])
    #time, voxel, specie
    data = np.array(my_file['trial0']['output']['__main__']['population'])
    subvolumes = list(my_file['model']['output']['__main__']['elements'])
    species = list(my_file['model']['output']['__main__']['species'])
    save_concentrations(my_file, fname[:-3])
