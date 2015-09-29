import random
import time

n_universe = 10000
n_assets = 1000
R_names = ["X" + str(x) for x in range(n_universe)]
R_values = [random.normalvariate(0, 1) for i in range(n_universe)]
W_names = ["X" + str(x) for x in random.sample(range(n_universe), n_assets)]
W_values = [random.normalvariate(0, 1) for i in range(n_assets)]

R = dict(zip(R_names, R_values))
W = dict(zip(W_names, W_values))

start = time.clock()
for n in range(5000):
    X = {}
    for v in W.keys():
        X[v] = W[v]*(R[v]+1)
print(time.clock() - start)
