import pandas as pd
import numpy as np
import random
import time

n_universe = 10000
n_assets = 1000
R_names = ["X" + str(x) for x in range(n_universe)]
R_values = np.random.normal(size=n_universe)

R = pd.Series(R_values, index=R_names)

W_names = ["X" + str(x) for x in random.sample(range(n_universe), n_assets)]
W_values = np.random.normal(size=n_assets)

W = pd.Series(W_values, index=W_names)

start = time.clock()
for n in range(5000):
    X = pd.concat([R, W], axis=1, join='inner')
    X = X.rename(columns={0: 'ret', 1: 'weight'})
    X['out'] = (X['ret'] + 1) * X['weight']
print(time.clock() - start)


R = dict(zip(R_names, R_values))
W = dict(zip(W_names, W_values))

start = time.clock()
for n in range(5000):
    X = {}
    for v in W.keys():
        X[v] = W[v]*(R[v]+1)
print(time.clock() - start)
