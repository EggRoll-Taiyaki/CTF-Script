#!/usr/bin/env pypy3
import secrets
import signal
import hashlib

def tropical_pow(x, y, op):
    if 1 == y:
        return x
    exp = bin(y)
    value = x
 
    for i in range(3, len(exp)):
        value = op(value, value)
        if(exp[i:i+1]=='1'):
            value = op(value, x)
    return value

def _add(*a):
	return max(c for c in a) 

_add_semi = lambda a, b, c: _add(a, b)

def pair_add(*a):
    return (max(c[0] for c in a), max(c[1] for c in a))

pair_add_semi = lambda a,b,c: pair_add(a, b)

def _mul(a, b):
	return a + b

def pair_mul(a, b):
    return (max(a[0] + b[0], a[1] + b[1]), max(a[0] + b[1], a[1] + b[0]))

def _mul_semi(a, b, c):
	return a + b + c

def pair_mul_semi(a, b, c):
    return (max(c + a[0] + b[0], c + a[1] + b[1]), max(c + a[0] + b[1], c + a[1] + b[0]))

def semi_factory(c):
    def pair_mul_mat(a, b):
        zb = list(zip(*b))
        return [[pair_add(*[pair_mul_semi(x, y, c) for x, y in zip(row, col)]) for col in zb] for row in a]
    return pair_mul_mat

def _mul_mat(a, b):
	zb = list(zip(*b))
	return [[_add(*[_mul(x, y) for x, y in zip(row, col)]) for col in zb] for row in a]

def pair_mul_mat(a, b):
    zb = list(zip(*b))
    return [[pair_add(*[pair_mul(x, y) for x, y in zip(row, col)]) for col in zb] for row in a]


### Homomorphism

def H(Z):

	n = len(Z)
	_Z = [[None for j in range(2 * n)] for i in range(2 * n)]
	for i in range(n):
		for j in range(n):
			_Z[2 * i][2 * j] = Z[i][j][0]
			_Z[2 * i + 1][2 * j + 1] = Z[i][j][0]
			_Z[2 * i][2 * j + 1] = Z[i][j][1]
			_Z[2 * i + 1][2 * j] = Z[i][j][1]
			
	return _Z

def inv_H(Z):

	n = len(Z)
	assert n % 2 == 0
	_Z = [[None for j in range(n // 2)] for i in range(n // 2)]
	for i in range(n // 2):
		for j in range(n // 2):
			_Z[i][j] = (Z[2 * i][2 * j], Z[2 * i][2 * j + 1])

	return _Z 

def luck_test(X, Y, A_pub, B_pub, t):

	_X, _Y, _A_pub = H(X), H(Y), H(A_pub)

	Xs, Ys = [_X], [_Y]
	for t1 in range(1, t):
		Xs += [_mul_mat(Xs[-1], _X)]
		Ys += [_mul_mat(Ys[-1], _Y)]

	DIMENSION = len(X)
	Found = False
	for t1 in range(t):
		for t2 in range(t):
			tmp = _mul_mat(Xs[t1], Ys[t2])
			shift = _A_pub[0][0] - tmp[0][0]
			v = True
			for i in range(DIMENSION):
				for j in range(DIMENSION):
					if _A_pub[i][j] - tmp[i][j] != shift:
						v = False
						break
				if not v:
					break
			if v:
				return inv_H(Xs[t1]), inv_H(Ys[t2]), shift
