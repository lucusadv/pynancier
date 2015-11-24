import multifold as mf

def test_reader():
	A = mf.reader('returns.csv')
	x = next(A)
	assert x.date == '2014-11-19'


def test_scalar():
	x = {'a':1, 'b': 2, 'c':-1}
	y = {'a':-1, 'b': 10}
	v = mf.dotprod(x, y)
	w = mf.dotprod(x, y, f = lambda x, y: y / x)
	assert v == 19
	assert w == 4
	
