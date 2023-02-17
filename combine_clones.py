import pandas as pd
import os

clones = [f for f in os.listdir() if "_clones.txt" in f]
df = pd.read_csv(clones[0], sep='\t')
df.reset_index(inplace=True, drop=True)
df['source'] = clones[0]

for cfile in clones[1:]:
    n_df = pd.read_csv(cfile, sep='\t')
    n_df.reset_index(inplace=True, drop=True)
    n_df['source'] = cfile
    df = df.append(n_df)
df.sort_values(by=['source','Clone fraction'], ascending=[True, False],inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_csv('all_clones.csv')

