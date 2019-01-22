import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
forb_list = ['PKAcAMP4_PDE4B','PKAcAMP4_PDE4D','PKAcAMP2','PKAcAMP4','PKAcAMP4_I1','PKAcAMP4_GluR1','PKAcAMP4_GluR1_S831',]
PP_list = ['Ip35PP1','Ip35PP1PP2BCaMCa4','Ip35PP2BCaMCa4']
def Parser():
  parser = argparse.ArgumentParser(description='Generation of figures')
  parser.add_argument('input',nargs='+',
                      help='input files')
  parser.add_argument('--labels',  default=None,
                      help='File labels')
  parser.add_argument('--units', default='[nM/l^3]',
                      help='concentration units')
  parser.add_argument('--output_name', default='',
                      help='name of the output files')
  return parser

if __name__ == '__main__':
    fname=[]
    args = Parser().parse_args()
    for name in args.input: 
        fname.append(name)
    if not fname:
        sys.exit('Do specify at least one totals filename')
    
    header = []
    longest = ''
    species = set()
    for name in fname:
        try:
            f = open(name)
        except IOError:
            sys.exit('Could not read '+fname)
        head = f.readline()
        header.append(head.split())
        for specie in head.split()[1:]:
            species.add(specie)
        f.close()

    data = []
    pkac = []
    pp2b = []
    if args.output_name:
        output = args.output_name
    else:
        output = ''
        for item in fname[-1].split('-')[:-1]:
          output += item
          output += '-'
    if args.labels:
        args.labels = args.labels.split(',')
        if len(args.labels) != len(fname):
            args.labels = None

    for i,name in enumerate(fname):
        try:
            data.append(np.loadtxt(name,skiprows=1))
        except:
            print 'Empty file', name
            sys.exit()
        pkac.append(np.zeros(data[i][:,0].shape))
        pp2b.append(np.zeros(data[i][:,0].shape))
        
    for specie in species:
        print specie
        how_many = 0
        which = []
        which_header = []
        for k,head in enumerate(header):
          if specie in head:
            how_many += 1
            which.append(head.index(specie))
            which_header.append(k)
        f, axrr = plt.subplots(how_many,sharex=True)
        if how_many == 1:
          axrr = [axrr]

        for i in range(how_many):
          j = which_header[i]
          axrr[i].plot(data[j][:,0]/1000,data[j][:,which[i]])
          axrr[i].set_ylim(0, 1.05*data[j][:,which[i]].max())
          start, end = axrr[i].get_ylim()
          #axrr[i].yaxis.set_ticks(np.arange(start, end, (end-start)/3.))
          if args.labels:
            axrr[i].set_ylabel(args.labels[i])
          else:
            where = fname[j].split('_')[-1]
            axrr[i].set_ylabel(where)
          if 'PKAc' in specie and specie not in forb_list:
            pkac[j] +=  data[j][:,which[i]]
          # if specie == 'Ca':
          #   axrr[i].set_yscale('log')
          #   axrr[i].set_ylim(10,1.05*data[j][:,which[i]].max())
          if specie in PP_list:
            pp2b[j] += data[j][:,which[i]]
        axrr[how_many-1].set_xlabel('time [s]')
        axrr[0].set_title(specie+' '+args.units)

        f.savefig(output+'_'+specie+'.png',format='png')
        
    how_many = len(fname)
    which_header = range(how_many)
    f, axrr = plt.subplots(how_many,sharex=True)
    if how_many >1:
        for i in range(how_many):
            j = which_header[i]
            axrr[i].plot(data[j][:,0]/1000,pkac[j])
            axrr[i].set_ylim(0, 1.05*pkac[j].max())
            start, end = axrr[i].get_ylim()
            #axrr[i].yaxis.set_ticks(np.arange(start, end, (end-start)/3.))
            if args.labels:
                axrr[i].set_ylabel(args.labels[i])
            else:
                where = fname[j].split('_')[-1]
                axrr[i].set_ylabel(where)
            

        axrr[how_many-1].set_xlabel('time [s]')
        axrr[0].set_title('Total PKAc '+args.units)
        f.savefig(output+'_total_PKAc.png',format='png')
    else:
        
        j = which_header[i]
        axrr.plot(data[j][:,0]/1000,pkac[j])
        axrr.set_ylim(0, 1.05*pkac[j].max())
        
        if args.labels:
            axrr.set_ylabel(args.labels[0])
        else:
            where = fname[j].split('_')[-1]
            axrr.set_ylabel(where)
        where = fname[j].split('_')[-1]
        axrr.set_ylabel(where)

        axrr.set_xlabel('time [s]')
        axrr.set_title('Total PKAc '+args.units)
        f.savefig(output+'_total_PKAc.png',format='png')
    

 
