import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mol', help='molar mass', type=float)
parser.add_argument('--unit', help='micro or nano')
parser.add_argument('--volume', help='volume in microns', type=float)
args = parser.parse_args()

if args.unit == 'micro':
    unit = 1e-6
elif args.unit == 'nano':
    unit = 1e-9
else:
    raise AttributeError("Unit can be only 'micro' or 'nano'")
v = args.volume*1e-15

particles = args.mol*unit*6.022e23*v

print('volume', v)
print('Particles:', round(particles))

