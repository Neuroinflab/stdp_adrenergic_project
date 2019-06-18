#-*- coding: utf-8 -*-
from __future__ import division, print_function
import sys
import random
import argparse
import os.path
try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    sys.exit("Do install lxml")

fname = "100_Hz_basis.xml"
inj_list = ["onset", "rate", "duration", "period", "interTrainInterval",
            "numTrains", "end"]
inj_dict = {"onset": "",
            "duration": "",
            "rate": "",
            "period": "",
            "end": "",
            "interTrainInterval": "",
            "numTrains": "",
            "region":"",
}


def xml_root(filename):
    '''get root of an xml file. 
    '''
    tree = etree.parse(filename)
    root = tree.getroot()
    return root


def xml_write_to_file(filename, root):
    '''
    write xml tree to a file
    '''
    f = open(filename,'w')
    f.write(etree.tostring(root, pretty_print=True))

def read_in_entry(entry):
    values = dict()
    for child in entry:
        if '.' in child.text:
            values[child.tag] = float(child.text)
        else:
            values[child.tag] = int(child.text)
            
def parse_root(root):
    specie_inj = {}
    for son in root:
        if son.get('SpecieId') not in specie_inj:
            specie_inj[son.get('SpecieId')] = []
        values = read_in_entry(son)
        specie_inj[son.get('SpecieId')].append(values)
    return specie_inj
    
def read_in_file(filename):
    root = xml_root(filename)
    return parse_root(root)
    
def increase_values(specie_inj, specie, what, multiplier=1., addition=0.):

    if specie not in specie_inj:
        print('Unknown')
        return
    if isinstance(what, str):
        what = [what]
    new_specie_inj = specie_inj[specie].copy()
    for inj in new_specie_inj:
        for val in what:
            inj[val] = inj[val]*multiplier + addition
    return new_specie_inj

def append_new_train(old_specie_inj, new_train, specie):
    old_specie_inj[specie].append(new_train)

    
def change_1_HFS_train(root, specie, what, region=None, multiplier=1, addition=0, randomness=True):
    counter = 0
    previous_onset = 0
    for son in root:
        do = True
        if son.get('specieID') == specie:
            if region is None or region == son.get("injectionSite"):
                counter += 1
                if randomness and counter > 50:
                    rand = random.random()
                    if rand <= .5:
                        do = False

                for grandson in son:
                    if grandson.tag == "onset":
                        onset = float(grandson.text)
                        if onset > previous_onset +  3000:
                            counter = 0
                    if grandson.tag == what:
                        if '.' in grandson.text:
                            new_value = float(grandson.text)
                        else:
                            new_value = int(grandson.text)
                        if do:
                            new_value = multiplier*new_value + addition
                        else:
                            new_value = 0
                        grandson.text = str(new_value)
    return root
        

    
if __name__ == "__main__":
    root = xml_root(fname)
    new_root = change_1_HFS_train(root, "Ca", "rate",
                                  region="sa1[0].pointA",
                                  multiplier=2.5,
                                  addition=0)
    new_root = change_1_HFS_train(new_root, "CaB", "rate",
                                  region="sa1[0].pointA",
                                  multiplier=2.,
                                  addition=0)
    xml_write_to_file("HFS.xml", new_root)
