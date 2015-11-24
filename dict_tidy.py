# Grammar of data for dictionaries.
# This is supposed to be much slower than pandas, but more flexible and portable
from toolz import groupby
from operator import itemgetter
import re

def parser_(s):
  """
  Parses a string of comma-separated substrings.

  >>> parser_('a, b')
  (['a', 'b'], [])
  >>> parser_('-a, -b')
  ([], ['a', 'b'])
  >>> parser_(([], ['b', 'd']))
  ([], ['b', 'd'])

  Parameters
  ----------
  s: one of two inputs. Either a string of the form containing comma-separated strings, possibly beginning
  with a '-' sign; or a 2-ple of two lists of strings.

  Returns
  -------
  a tuple of two lists of strings
  """
  if type(s) == str:
    s = re.sub("\s*", "", s).split(',')
    var_sel = [x for x in s if not x.startswith('-')]
    var_unsel = [x[1:] for x in s if x.startswith('-')]
  else:
    var_sel, var_unsel = s
  assert not(len(var_sel) and len(var_unsel)),'select error: either exclude or include columns'
  assert len(var_sel) or len(var_unsel), 'select error: either exclude or include columns must be present'
  return(var_sel, var_unsel)



def select(df, s):
  incl, excl = parser_(s)
  if len(incl):
    new_keys =  incl
  else:
    new_keys = set(df.keys())
    new_keys = new_keys.difference(excl)
    print(new_keys)
  df2 = {k:df[k] for k in new_keys}
  return(df2)

def filter_list_int(x, i):
  """
  Filters list according to numerical indices.

  >>> list(filter_list_int([0, 1, 2, 3, 4], [0,2,3]))
  [0, 2, 3]
  """
  return(x[j] for j in i)


def filter_list_bool(x, b):
  """
  Filters list according to boolean indices.

  >>> list(filter_list_bool([0, 1, 2, 3, 4], [True, False, True, True, False]))
  [0, 2, 3]
  """
  return([y for y, cond in zip(x, b) if cond])


def filter(df, fn):
  b = fn(df)
  return{k: filter_list_bool(v, b) for (k, v) in df.items()}


def rank_list(x, reverse = False):
  """ 
  Returns a list with the rank of a list.

  >>> rank_list([3, 2, 1])
  [2, 1, 0]

  >>> rank_list([3, 2, 1], reverse = True)
  [0, 1, 2]
  """
  rank = [i for _, i in sorted(zip(x, range(len(x))), reverse = reverse)]
  return(rank)

def arrange(df, s):
  s = re.sub("\s*", "", s).split(',')
  s.reverse()
  for fld in s:
    if fld[0] == '-':
      fld = fld[1:]
      index = rank_list(df[fld], reverse = True)
    else:
      index = rank_list(df[fld], reverse = False)
    df = {k:[v[i] for i in index] for k, v in df.items()}
  return(df) 

def group_by(df, s):
#  s = re.sub("\s*", "", s).split(',')
  keys = zip(*select(df, s).values())
  y = zip(keys, range(10000))
  grouped_keys = groupby(itemgetter(0), y)
  for g in grouped_keys:
    index = g[1]
    yield filter_index(df, index)
    


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
  x = {'X1':[10, 2, 2, 4], 'X2':['a', 'z', 'b', 'd'],'X3':[-1, 2, 3, 0]}
  x_l = list(range(10))
  print(arrange(x, 'X1,X2'))
  _test()



