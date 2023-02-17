"""
Plot proportion of blanks vs. clone read count based on false reads from decoy wells that had no cells

What value of read count cutoffs include what % of total blanks?
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
pal = sns.color_palette(["#b6d3b3",
"#c8b7d7"])
sns.set_theme(context='notebook', style='ticks', palette=pal)

df = pd.read_pickle('../00_fastq/concatenated_clones.pkl')
df = df[df['plate'] == '100c/w']

def calcProportion(dframe):
    """

    :param dframe: subsetted df
    :return: numpy array of x and y values
    """
    n_total_blanks = dframe['Clone count'].sum()
    x_vals = np.linspace(1, dframe['Clone count'].max()+1,
                     int(dframe['Clone count'].max())+1)
    y_cutoff = np.array([dframe[dframe['Clone count'] >= x]['Clone count'].sum()
                         for x in x_vals])
    y_cutoff = y_cutoff/n_total_blanks #convert to fraction
    return [x_vals, y_cutoff]


blank_df = df[df['blank']]
nonblank_df = df[df['blank'] == False]

blank_calcs = calcProportion(blank_df)
nonblank_calcs = calcProportion(nonblank_df)

sns.lineplot(x=nonblank_calcs[0], y=nonblank_calcs[1], palette=pal, linewidth=2,
             label='Nonblank')
sns.lineplot(x=blank_calcs[0], y=blank_calcs[1], palette=pal, linewidth=2,
             label='Blank')

sns.despine()
plt.legend()
plt.ylabel('Proportion of reads')
plt.xlabel('Clone read count cutoff')
plt.xlim(-10, 1000)

plt.savefig('proportionBlank_vs_reads.png', dpi=300)
plt.savefig('proportionBlank_vs_reads.eps')
