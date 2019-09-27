#!/usr/bin/env python
from __future__ import print_function, division, unicode_literals
import h5py
import numpy as np
from lxml import etree
import sys
from scipy.constants import Avogadro

NA = Avogadro*1e-23
spine = ['PSD', 'head', 'neck']


def nano_molarity(N, V):
    return 10 * N / V / NA


def pico_sd(N, S):
    return 10 * N / S / NA


def get_grid_list(My_file):
    return np.array(My_file['model']['grid'])


def get_times(My_file, trial='trial0', output="__main__"):
    return np.array(My_file[trial]['output'][output]['times'])

def get_outputs(my_file):
    return my_file['model']['output'].keys()


def get_populations(my_file, trial='trial0', output='__main__'):
    return np.array(my_file[trial]['output'][output]['population'])


def get_all_species(My_file, output="__main__"):
    return [s.decode('utf-8') for s in My_file['model']['output'][output]['species']]


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
                        if name in all_anchored_species:
                            anchored.append(name)
    return list(set(anchored))

def get_output_regions(my_file):
    root = etree.fromstring(my_file['model']['serialized_config'][0])
    outputs = {}
    for son in root:
        if son.tag.endswith('OutputScheme'):
            for grandson in son:
                outputs[grandson.get("filename")] = grandson.get("region")
    return outputs
        
def get_key(cell):
    return cell[15].decode('utf-8') + '_' + cell[18].decode('utf-8')

def region_volumes(my_file):
    grid_list = get_grid_list(my_file)
    regions = get_regions(my_file)
    volumes = {}
    for region in regions:
        volumes[region] = 0
    for cell in grid_list:
        key = get_key(cell)
        volumes[key] += float(cell[12])
    return volumes


def sum_volume(my_file, region_list):
    grid_list = get_grid_list(my_file)
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
                width = abs(grid_list[cell_idx][0] - grid_list[cell_idx][3])
                surface[key] += depth * width
            else:
                print('Unimplemented direction', direction)
    return surface


def get_region_indices(my_file):
    grid_list = get_grid_list(my_file)
    region_ind = {}
    for idx, cell in enumerate(grid_list):
        key = get_key(cell)
        if key not in region_ind:
            region_ind[key] = []
        region_ind[key].append(idx)
    return region_ind

def get_spines(regions):
    out = {}
    for region in regions:
        try:
            end = region.split("_")[1]
        except IndexError:
            continue
        if end == "":
            continue

        if end in out:
            out[end].append(region)
        else:
            out[end] = [region]
    return out


def get_regions(my_file):
    grid_list = get_grid_list(my_file)
    return sorted(list(set([get_key(grid) for grid in grid_list])))


def get_concentrations_region_list(my_file, my_list, trial, out):

    grid_list = get_grid_list(my_file)
    species = get_all_species(my_file)
    idxs = sum_indices(my_file, my_list)
    vol = sum_volume(my_file, my_list)
    data = get_populations(my_file, trial=trial, output=out)
    numbers = data[:, idxs, :].sum(axis=1)
    return nano_molarity(numbers, vol)


def get_concentrations(my_file, trial, out):
    grid_list = get_grid_list(my_file)
    data = get_populations(my_file, trial=trial, output=out)
    species = get_all_species(my_file, output=out)
    regions = get_regions(my_file)
    submembrane_species = get_all_submembrane_species(my_file)
    volume_dict = region_volumes(my_file)
    surface_dict = region_surface(grid_list)
    concentrations = np.zeros((data.shape[0], len(regions), len(species)))
    numbers = np.zeros_like(concentrations)
    region_indices = get_region_indices(my_file)

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
    return concentrations


def save_single_file(times, concentrations, species, fname):
    header = 'time'
    for specie in species:
        header += ' ' + specie
    what_to_save = np.zeros((concentrations.shape[0], len(species) + 1))
    what_to_save[:, 0] = times[:concentrations.shape[0]]
    what_to_save[:, 1:] = concentrations
    print(fname)
    np.savetxt(fname, what_to_save, header=header, comments='')


def save_concentrations(my_file, fname_base, output, trial='trial0'):
    regions = get_regions(my_file)
    times = get_times(my_file, trial=trial, output=output)
    species = get_all_species(my_file, output=output)
    concentrations = get_concentrations(my_file, trial, output)
    if output == '__main__':
        add = ''
    else:
        add = output + '_'
    for i, region in enumerate(regions):
        fname = '%s_%s%s_%s.txt' % (fname_base, add, trial, region)
        save_single_file(times, concentrations[:, i, :], species, fname)
    if len(regions) > 1:
        totals = get_concentrations_region_list(my_file, regions, trial, output)
        save_single_file(times, totals, species, '%s_%s%s_%s.txt' % (fname_base, add, trial, 'total'))
        spines_dict = get_spines(regions)
        for spine_name in spines_dict.keys():
            spine_reg = spines_dict[spine_name]
            spine = get_concentrations_region_list(my_file, spine_reg,
                                                   trial, output)
            save_single_file(times, spine, species,
                             '%s_%s%s_%s.txt' % (fname_base, add,
                                                 trial, spine_name))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('No filename given')
    for fname in sys.argv[1:]:
        my_file = h5py.File(fname, 'r')
        output_dict = get_output_regions(my_file)
        for trial in my_file.keys():
            if trial != 'model':
                save_concentrations(my_file, fname[:-3], '__main__', trial=trial)
                for out in output_dict:
                    if output_dict[out] is None:
                        save_concentrations(my_file, fname[:-3], out, trial=trial)
                    
    print('Done')

