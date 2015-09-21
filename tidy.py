import re
import pandas as pd
from toolz import curry

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

@curry
def select(s, df):
  """
  Select columns in a data frame.

  >>> df = pd.DataFrame({"A":["foo", "foo", "foo", "bar"], "B":[0,1,1,0], "C":["A","A","B","A"]})
  >>> select('A', df)
       A
  0  foo
  1  foo
  2  foo
  3  bar
  """
  incl, excl = parser_(s)
  if len(incl):
    df2 = df[incl]
  else:
    df2 = df.drop(excl, axis=1)
  return(df2)

@curry
def filter(df, s):
  """
  Filter rows in a data frame using the query syntax.

  >>> df = pd.DataFrame({"A":["foo", "foo", "foo", "bar"], "B":[0,1,1,0], "C":["A","A","B","A"]})
  >>> filter(df, 'A in "bar"')
       A  B  C
  3  bar  0  A
  >>> filter(df, 'A not in "bar"')
       A  B  C
  0  foo  0  A
  1  foo  1  A
  2  foo  1  B

  Parameters
  ----------
  s: a string conforming with the syntax of the pandas.DataFrame.query method
  df: pandas DataFrame

  Returns
  -------
  A data frame
  """
  df2 = df.query(s)
  return(df2)

@curry
def arrange(df, s):
  """
  Sorts according to columns.

  Parameters
  ----------
  s: a string of the form 'a, -b, c, -d'
  df: a data frame

  Returns
  -------
  A data frame
  """
  asc, desc = parser_(s)
  order = [1] * len(asc) + [0] * len(desc)
  df2 = df.sort(columns = asc + desc, ascending = order, axis = 0)
  return(df2)

@curry
def distinct_all(df):
  """
  Returns only nonduplicated rows.

  Parameters
  ----------
  s: a string of the form 'a, -b, c, -d'
  df: a data frame

  Returns
  -------
  A data frame
  """
  df2 = df.drop_duplicates()
  return(df2)

@curry
def distinct(df, s):
  """
  Returns only nonduplicated rows.

  Non-duplication is considered only for the columns specified
  in the string.

  Parameters
  ----------
  s: a string of the form 'a, -b, c, -d'
  df: a data frame

  Returns
  -------
  A data frame
  """
  if s != '':
    cols, _ = parser_(s)
    df2 = df.drop_duplicates(cols)
  else:
    df2 = df.drop_duplicates()
  return(df2)

@curry
def group_by(df, s):
  """
  Groups by a data frame based values of one or more columns.

  Parameters
  ----------
  s: a string containing column names
  df: a data frame

  Returns
  -------
  A data frame
  """
  cols, _ = parser_(s)
  df2 = df.groupby(cols, as_index = False)
  return(df2)

@curry
def summarize(df, d):
  """
  Summarizes columns in data frames of a group_by object

  Parameters
  ----------
  d: a dictionary in which keys are column names and values are lambdas
  df: a data frame

  Returns
  -------
  A data frame
  """
  df2 = df.aggregate(d)
  return(df2)

@curry
def mutate(df, d):
  """
  mutate columns a in data frame

  >>> df = pd.DataFrame({"A":["foo", "foo", "foo", "bar"], "B":[0,1,1,0], "C":["A","A","B","A"]})
  >>> d = {'D': lambda x: x.B, 'E': lambda x: x.B + 0.5}
  >>> tmp = mutate(df, d)
  >>> select('E', tmp)
       E
  0  0.5
  1  1.5
  2  1.5
  3  0.5

  Parameters
  ----------
  df: a data frame
  d: a dictionary in which keys are column names and values are lambdas

  Returns
  -------
  A data frame

  """
  df2 = df.copy()
  for var, fn in d.items():
    df2[var] = fn(df)
  return(df2)

@curry
def gather(df, id_vars, value_vars, var_name, value_name):
  """
  Gathers data, treating column values as variables.

  >>> df = pd.DataFrame({"Name":["Jon", "Steven", "Seth", "Chelsea", "Amy"], "Male":[1,1,1,0,0], "Female":[0,0,0,1,1]})

  """
  id_vars, _ = parser_(id_vars)
  value_vars, _ = parser_(value_vars)
  if any(value_vars) and not any(id_vars):
    id_vars = list(set(df.columns).difference(value_vars))
  print(id_vars)
  df2 = pd.melt(df, id_vars, value_vars, var_name, value_name)
  return(df2)

@curry
def spread(df, index, columns, values):
  """
  Turns data frame into wide form.

  >>> df = pd.DataFrame({"Name":["Jon", "Steven", "John", "Chelsea", "Amy"], "Gender":['M','M','M','F','F'], "Funny":[0,0,0,1,1]})
  >>> spread(df, 'Name', 'Gender', 'Funny')['F']['Amy']
  1.0
  """
  df2 = df.pivot(index = index, columns = columns, values = values)
  return(df2)
if __name__ == "__main__":
  import doctest
  doctest.testmod()

def inner_join(left_on, right_on, df1, df2):
  df3 = df1.merge(df2, how='inner', left_on=left_on, right_on=left_on)
  return(df3)

def outer_join(left_on, right_on, df1, df2):
  df3 = df1.merge(df2, how='outer', left_on=left_on, right_on=left_on)
  return(df3)

def left_join(left_on, right_on, df1, df2):
  df3 = df1.merge(df2, how='left', left_on=left_on, right_on=left_on)
  return(df3)

def right_join(left_on, right_on, df1, df2):
  df3 = df1.merge(df2, how='right', left_on=left_on, right_on=left_on)
  return(df3)

@curry
def test(x, a=1, b=2):
    return(x+a+b)
    
