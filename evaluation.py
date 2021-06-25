import glob
import operator
import re
from functools import reduce
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

files = glob.glob('*.txt')

crack_tip_num = 4


# def get_param(df, start):
#     return reduce(operator.add, re.findall(r"(\d)", df.iloc[start::crack_tip_num][0]), '')


i = 0
final_results = {'file': [], 'k1': [], 'k2': [], 'g1': [], 'g2': []}    # , 'param': []

for file in files:

    i += 1
    # open and read file:
    with open(file) as f:
        content = f.readlines()
        # removing header of file:
        content = reduce(operator.add, content, "")

        # use regexp  for search "Y mouth" + 2 numbers, then grab two (maybe) float numbers
        # param = re.search(
        #    r"Y mouth\n *\d *\d *(\d*\.?\d*?) *(\d*\.\d*)\n *\d *\d *(\d*\.?\d*?) *(\d*\.\d*)\n *\d *\d *(\d*\.?\d*?) *(\d*\.\d*)\n *\d *\d *(\d*\.?\d*?) *(\d*\.\d*)",
        #    content)
        # print(param.groups())
        # not yet generalized:
        # final_results['param'].append(float(param.group(2))-float(param.group(6)))

        # extract information for each crack tip:
        for x in range(0, crack_tip_num):
            # use regexp for search, "Total" + 4 numbers with decimal point, do this for number of crack tips:
            result = re.search(r"Total *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+) *(-?\d+\.\d+)", content)

            final_results['file'].append(file)
            final_results['k1'].append(float(result.group(1)))
            final_results['k2'].append(float(result.group(2)))
            final_results['g1'].append(float(result.group(3)))
            final_results['g2'].append(float(result.group(4)))

        f.close()

# plotting:
df = pd.DataFrame(final_results)

# sorting dataFrame by filename:
df['sort'] = df['file'].str.extract(r'(\d+)', expand=False).astype(int)
df.sort_values('sort', inplace=True, ascending=False)
df = df.drop('sort', axis=1)
df.reset_index(drop=True, inplace=True)

# resorting df for each crack tip
# df['k1_1'] = df['k1'][::crack_tip_num]
# df['k1_2'] = df['k1'][1::crack_tip_num]

# changing SIF from MPa * sqrt(in) into MPa * sqrt(m):
df['k1'] = df['k1'] * np.sqrt(0.0254)

# plot sif at each crack tip:
df['k1'][::crack_tip_num].plot()
df['k1'][1::crack_tip_num].plot()
df['k1'][2::crack_tip_num].plot()
df['k1'][3::crack_tip_num].plot()
plt.legend(['crack number: ' + str(elem) for elem in range(0, crack_tip_num)])

plt.show()

'''
i = 0
for file in files:

    df[df['file'] == file].iloc[0][1]

    # extracting del_y from file name (not a pretty solution):
    df['del_y'] = reduce(operator.add, re.findall(r"(\d)", df[df['file'] == file].iloc[0][0]), '')
    i += 1
    
'''

print(df)

