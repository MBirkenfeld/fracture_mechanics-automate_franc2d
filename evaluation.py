import glob
import operator
import re
from functools import reduce
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


ksi2mpa = 0.14503773800722
in2mm = 25.4
N2pound = 4.4482216282509


def k_i(sigma, a):
    return sigma * ((np.pi * a / N2pound / 1000) ** 0.5)


# get file name in files:
files = glob.glob('*.txt')

# get number of crack tips(ideally you could import this from the file):
crack_tip_num = 4


# def get_param(df, start):
#     return reduce(operator.add, re.findall(r"(\d)", df.iloc[start::crack_tip_num][0]), '')


i = 0
final_results = {'file': [], 'k1': [], 'k2': [], 'g1': [], 'g2': [], 'param': []}

for file in files:

    i += 1
    # open and read file:
    with open(file) as f:
        content = f.readlines()
        # removing header of file:
        content = reduce(operator.add, content, "")

        # extract information for each crack tip:
        for x in range(0, crack_tip_num):
            # use regexp for search, "Total" + 4 numbers with decimal point, do this for number of crack tips:
            result = re.search(r"Total *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+)", content)

            # use regexp  for search "Y mouth" + 2 numbers, then grab two (maybe) float numbers:
            param = re.search(
                r"Y mouth *?\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n *\d *\d *(\d*\.?\d*?) *(\d*\.?\d*?)\n",
                content)

            # not yet generalized:
            final_results['param'].append(float(param.group(6)) - float(param.group(2)))
            final_results['file'].append(file)
            final_results['k1'].append(float(result.group(1)))
            final_results['k2'].append(float(result.group(2)))
            final_results['g1'].append(float(result.group(3)))
            final_results['g2'].append(float(result.group(4)))

        f.close()



# plotting:
df = pd.DataFrame(final_results)
df['k'] = [k_i(1000, 10)] * len(df['k1'])

# sorting dataFrame by filename:
df['sort'] = df['file'].str.extract(r'(\d+)', expand=False).astype(int)
df.sort_values('sort', inplace=True, ascending=False)
df = df.drop('sort', axis=1)
df.reset_index(drop=True, inplace=True)

# changing SIF from MPa * sqrt(in) into MPa * sqrt(m):
df['k1'] = df['k1'] * np.sqrt(0.0254) * ksi2mpa

# plot sif at each crack tip:
plt.plot(df['param'][::crack_tip_num], df['k1'][::crack_tip_num])
plt.plot(df['param'][1::crack_tip_num], df['k1'][1::crack_tip_num])
plt.plot(df['param'][2::crack_tip_num], df['k1'][2::crack_tip_num])
plt.plot(df['param'][3::crack_tip_num], df['k1'][3::crack_tip_num])
plt.plot(df['param'], df['k'])
plt.legend(['sif mode 1 crack tip number ' + str(elem) for elem in range(1, crack_tip_num+1)] + ['sif_analytic'])
plt.show()

plt.plot(df['param'][::crack_tip_num], df['k2'][::crack_tip_num])
plt.plot(df['param'][1::crack_tip_num], df['k2'][1::crack_tip_num])
plt.plot(df['param'][2::crack_tip_num], df['k2'][2::crack_tip_num])
plt.plot(df['param'][3::crack_tip_num], df['k2'][3::crack_tip_num])
plt.legend(['sif mode 2 crack tip number ' + str(elem) for elem in range(1, crack_tip_num+1)])

plt.show()

print(df)

