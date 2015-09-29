import random

def rotate(x, shift, base):
	if shift >= 0:
		if x + shift < base:
			x=x+shift
		else:
			x=x+shift-base
	else:
		if x + shift >= 0:
			x=x+shift
		else:
			x=x+shift+base
	return(x)


def encr(f, seed=31459):
	random.seed(seed)
	out=''
	for n in f:
		r=random.randrange(0,128)
		n2 = rotate(ord(n), r, 128)
		out=out + str(n2) + ','
	out=out[0:-1]
	return(out)

def decr(f, seed=31459):
	f = f.split(',')
	random.seed(seed)
	out=''
	for n in f:
		r=random.randrange(0,128)
		n2 = rotate(int(n), -r, 128)
		out=out + chr(n2)
	return(out)


if __name__ == '__main__':
	s=''.join([chr(x) for x in range(0,128)])
	check=[decr(encr(s, seed=x), seed=x)==s for x in random.sample(range(2**10), 1000)]
	print('check passed on multiple decriptions:', all(check))
	teststring=open('encdec.py','r').read()
	print('check passed on test code:', decr(encr(teststring))==teststring)
