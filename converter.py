import pandas as pd
import numpy as np
import os 
import glob
import fnmatch
import re

# check how to make these relative paths
stockdir = '/Users/gappy/dropbox/kernel_data/market/US'
stockfnames = [ 'mktcap.txt', 'tradingvolume.txt', 'priceclose.txt']

loadir   = '/Users/gappy/dropbox/kernel_data/fundamental/US'
loadfnames = [ 'LOADINGS.txt']

fundir   = '/Users/gappy/dropbox/kernel_data/security'

def to_pickle(path, fnames):
  for f in fnames:
    DF = pd.read_csv(os.path.join(path, f), sep='|')
    f_out = f.split('.')[0] + '.pkl'
    DF.to_pickle(os.path.join(path, f_out))


to_pickle(stockdir, fnames)

fnames = ['totret.txt', 'divs.txt', 'mktcap.txt', 'vol.txt', 'price.txt']




