import glob
import operator
import re
from functools import reduce
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


ksi2mpa = 6.89
in2mm = 25.4
# N2pound = 4.4482216282509
ksi_in2mpa_m = 1.099



def k_i(sigma, a):
    return sigma * ksi2mpa * np.sqrt(np.pi * a / 1000)


# get file name in files:
files = glob.glob('*.txt')

# get number of crack tips(ideally you could import this from the file):
crack_tip_num = 4


# def get_param(df, start):
#     return reduce(operator.add, re.findall(r"(\d)", df.iloc[start::crack_tip_num][0]), '')


i = 0
final_results = {'file': [], 'param': []}

for file in files:

    i += 1
    # open and read file:
    with open(file) as f:
        content = f.readlines()
        # removing header of file:
        content = reduce(operator.add, content, "")

        # extract information for each crack tip:
        # use regexp for search, "Total" + 4 numbers with decimal point, do this for number of crack tips:
        result = re.findall(r"Total *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+)", content)

        # use regexp  for search "Y mouth" + 2 numbers, then grab two (maybe) float numbers:
        param = re.findall(
                r"Y mouth *?\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n",
                content)
        final_results['param'].append(float(param[0][5]) - float(param[0][1]))
        final_results['file'].append(file)

        j = 0
        for crack in result:
            j += 1
            # not yet generalized:
            final_results.setdefault('k1_' + str(j), []).append(float(crack[0]))
            final_results.setdefault('k2_' + str(j), []).append(float(crack[1]))
            final_results.setdefault('g1_' + str(j), []).append(float(crack[2]))
            final_results.setdefault('g2_' + str(j), []).append(float(crack[3]))
        f.close()

print(len(final_results['k1_1']))

# plotting:
df = pd.DataFrame(final_results)
df['k1'] = [k_i(100, 10)] * len(df['k1_1'])
df['k2'] = df['k1'] * 0


# sorting dataFrame by filename:
df['sort'] = df['file'].str.extract(r'(\d+)', expand=False).astype(int)
df.sort_values('sort', inplace=True, ascending=False)
df = df.drop('sort', axis=1)
df.reset_index(drop=True, inplace=True)

df['param'] = df['param'] * in2mm
df = df.set_index('param')

# selecting labels to plot:
ks1 = ['k1_' + str(elem) for elem in range(1, crack_tip_num+1)]
ks2 = ['k2_' + str(elem) for elem in range(1, crack_tip_num+1)]

# changing SIF from ksi * sqrt(in) into MPa * sqrt(m):
df[ks1] = df[ks1] * ksi_in2mpa_m
df[ks2] = df[ks2] * ksi_in2mpa_m



# plot sif at each crack tip:
df[ks1].plot()
plt.plot(df['k1'])

plt.legend(['crack tip number ' + str(elem) for elem in range(1, crack_tip_num+1)] + ['sif_analytical'])
plt.title('sif mode 1')
plt.xlabel('delta y in mm')
plt.ylabel('sif in Mpa*sqrt(m)')
plt.show()

df[ks2].plot()
df['k2'].plot()
plt.legend(['crack tip number ' + str(elem) for elem in range(1, crack_tip_num+1)] + ['sif_analytical'])
plt.title('sif mode 2')
plt.xlabel('delta y in mm')
plt.ylabel('sif in Mpa*sqrt(m)')
plt.show()

print(df)

