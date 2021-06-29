import glob
import operator
import re
from functools import reduce
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

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
            print(file)
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


# final_results['param_ph'] = []
# for elem in final_results['param']:
#     for i in range(1, 4):
#         final_results['param_ph'].append(elem)
# final_results['param'] = final_results['param_ph']
# final_results['param'] = 4 * final_results['param']

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
plt.plot(df['param'][::crack_tip_num], df['k1'][::crack_tip_num])
plt.plot(df['param'][1::crack_tip_num], df['k1'][1::crack_tip_num])
plt.plot(df['param'][2::crack_tip_num], df['k1'][2::crack_tip_num])
plt.plot(df['param'][3::crack_tip_num], df['k1'][3::crack_tip_num])

plt.legend(['crack tip number: ' + str(elem) for elem in range(1, crack_tip_num+1)])

plt.show()

print(df)

