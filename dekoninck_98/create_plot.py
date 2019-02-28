import os
import pandas as pd
import matplotlib.pyplot as plt


def get_ck(df):
    result = 0
    for c in df.columns:
        if 'CKp' in c:
            result += df[c].iloc[-1]
    return result


csvs = [i for i in os.listdir(os.path.dirname(__file__))
        if 'model_start_trial0' in i and not i.startswith('.~') and '5uM' not in i]

df = pd.read_csv('model_start_trial0_dendrite_5000nM_3s.csv')
max_phospho = get_ck(df)

all_phospho = []
for c in csvs:
    df = pd.read_csv(c)
    ckp_value = (get_ck(df) / max_phospho) * 100
    #ckp_value = pd.read_csv(c)['CKp'].iloc[-1]
    cam_molar_injection = int(float(c.replace('model_start_trial0_dendrite_', '').replace('nM_3s.csv', '')))
    all_phospho.append((ckp_value, cam_molar_injection))

x, y = zip(*sorted(all_phospho, key=lambda a: a[1]))

fix, ax = plt.subplots()
ax.semilogx(y,x, 'ro', linestyle='--')
ax.grid()
ax.set(ylabel='CaMKII autophosphorylation (% maximal)', xlabel='CaM injection (nM)',
       title='100% is CaMKII autophosphorylation at 5000nM of CaM injection through 50ms. Sim for 6000ms')
plt.show()