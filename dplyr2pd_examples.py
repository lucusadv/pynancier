import pandas as pd
from dplyr2pd import *
first = ['Bob','Jessica','Mary','John','Mel']
births = [1960, 1550, -2939, 5, 1920]
last = ['Smith', 'Chastain', 'Magdalene', 'Cleese', 'Brooks']
BabyDataSet = zip(first, last, births)
df = pd.DataFrame(data = list(BabyDataSet), columns=['First', 'Last', 'Births'])
df2 = pd.DataFrame({"A":["foo", "foo", "foo", "bar"], "B":[0,1,1,0], "C":["A","A","B","A"]})


