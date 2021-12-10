import numpy as np
import pandas as pd
import json
import glob
import os
import matplotlib.pyplot as plt

def comp(x, y):
    if 1 ==x !=y:
        return 'lsm'
    if 1 ==y !=x:
        return 'mlm'
    if 1 ==y ==x:
        return 'same'
    return None

def show_diff(s_res, m_res, lang):
    mbetter = []
    sbetter = []

    df = pd.merge(s_res,m_res,how='outer', suffixes=('_lsm', '_mlm'), on=['prompt', 'sub_label', 'obj_label'])
    df['better'] = np.vectorize(comp)(df['correct_lsm'], df['correct_mlm'] )
    df.drop(['correct_lsm', 'correct_mlm'], axis=1, inplace=True)

    sbr = len(df[df['better']=='lsm'])/len(df)
    mbr = len(df[df['better']=='mlm'])/len(df)
    samer = len(df[df['better']=='same'])/len(df)

    return mbr, sbr, samer, df

def plot_bar(groups, lg, ticks, filename):
    # Width of a bar 
    width = 0.3       
    N = len(ticks)
    ind = np.arange(N)
    print(plt.style.available)
    # plt.style.use('seaborn-li')

    # Plotting
    for i, gp in enumerate(groups):
        plt.bar(ind + i*width, gp, width, label=lg[i])

    plt.xticks(ind + width / 2, ticks)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(filename+'.jpg', dpi=100)
    plt.show()
