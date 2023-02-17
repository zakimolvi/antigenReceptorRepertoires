"""
What is the count* for each CDR3a,b that we consider to be a true identification?

*Count refers to # of wells each CDR3 was observed in
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
pal = sns.color_palette(["#b6d3b3"])
sns.set_theme(context='notebook', style='ticks', palette=pal)

df = pd.read_pickle('../00_fastq/concatenated_clones.pkl')

#only non-blank reads from 100c/w plate passing read cutoff
df = df[df['plate'] == '100c/w']
df = df[df['blank'] == False]
df = df[df['Clone count'] >= 100] #cutoff
df = df.sort_values(by='Clone count', ascending=False)

#drop any non-TRAV/TRBV reads
searchfor = ['TRAV', 'TRBV']
df = df[df['All V hits with score'].str.contains('|'.join(searchfor))]
df['chain'] = df['All V hits with score'].str.contains('TRAV').map({True:'TRAV',
                                                                    False:'TRBV'})
#export df
df.to_csv('filtered_clones.csv')
df.to_pickle('filtered_clones.pkl')

g = sns.catplot(x='AA. Seq. CDR3', data=df,
                col = 'chain', kind='count',
                order = df['AA. Seq. CDR3'].value_counts().index,
                palette=pal, height=4, aspect=0.75, sharex=False)

g.set_xticklabels(size=4.75, rotation=90)
g.axes[0][0].set_xlabel('')
g.axes[0][0].set_title(r'CDR3$\alpha$')
g.axes[0][1].set_xlabel('')
g.axes[0][1].set_title(r'CDR3$\beta$')
g.axes[0][0].set_ylabel('Number of wells observed in')

plt.tight_layout()
plt.savefig('CDR_counts.png', dpi=300)
