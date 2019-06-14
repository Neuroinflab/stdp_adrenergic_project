#-*- coding: utf-8 -*-
from __future__ import division
import subprocess
import collections
import sys
import random
import argparse
import re
import numpy as np
import os.path
try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    sys.exit("Do install lxml")

fname = "100_Hz_basis.xml"

inj_dict = {"onset": "",
            "duration": "",
            "rate": "",
            "period": "",
            "end": "",
            "interTrainInterval": "",
            "numTrains": "",
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

    
def change_1_HFS_train(root, specie, what, multiplier=1, addition=0):
    for son in root:
        if son.get('specieId') == specie:
            for grandson in son:
                if grandson.tag == what:
                    if '.' in granson.text:
                        new_value = float(granson.text)
                    else:
                        new_value = int(granson.text)
                    new_value = multiplier*new_value + addition
                    grandson.text = str(new_value)
    return root
        

    
if __name__ == "__main__":
    root = xml_root(fname)
    print(root)
    new_root = change_1_HFS_train(root, "Ca", "rate", 0.5, 0)
    xml_write_to_file("HFS.xml", root)
