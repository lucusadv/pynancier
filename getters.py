import pandas as pd
import numpy as np
import os 
import glob
import fnmatch
import re

# check how to make these relative paths
stockdir = '/Users/gappy/dropbox/kernel_data/market/US'
stockfnames = [ 'totret.txt', 'mktcap.txt', 'tradingvolume.txt']
loadir   = '/Users/gappy/dropbox/kernel_data/loadings'
fundir   = '/Users/gappy/dropbox/kernel_data/fundamental'



def to_pickle(path, fnames):
  for f in fnames:
    DF = pd.read_csv(os.path.join(path, f), sep='|')
    f_out = f.split('.')[0] + '.pkl'
    DF.to_pickle(os.path.join(path, f_out))

if __name__ == '__main__':
  fnames = [ 'mktcap.txt', 'tradingvolume.txt', 'priceclose.txt']
  to_pickle(stock_dir, stock_fnames)






