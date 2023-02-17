"""
Plot summary stats for reads from MiXCR concatenated clones
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pal = sns.color_palette(["#b6d3b3",
"#c8b7d7"])

sns.set_theme(context='notebook', style='ticks', palette=pal)
df = pd.read_pickle('../00_fastq/concatenated_clones.pkl')
df = df.sort_values(by='Clone count', ascending=False)

g = sns.catplot(x='sort_well', y='Clone count', hue='blank', row='plate',
            data=df, edgecolor='k',
            legend_out=True, height=4, aspect=1.5)

g.set_xticklabels(size=4, rotation=90)
g.axes[0][0].set_ylabel('clone read count')
g.axes[1][0].set_ylabel('clone read count')

plt.yscale('log')
plt.xlabel('well')

plt.savefig('well_counts.png', dpi=300)
plt.savefig('well_counts.eps')
