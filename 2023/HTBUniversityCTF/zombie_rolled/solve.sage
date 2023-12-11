from output import *
from Crypto.Util.number import *
from fractions import Fraction
from math import prod
from hashlib import sha256
import sys

##############################
# Guess prime factors by Magic :>
##############################

def magic(a, b, c):
	return Fraction(a, b) + Fraction(b, c) + Fraction(c, a)

x, y, z = pub
gxy, gyz, gzx = GCD(x, y), GCD(y, z), GCD(z, x)

_x = x // gxy // gzx
_p = abs(gzx // _x)

_y = y // gyz // gxy
_q = abs(gxy // _y)

_z = z // gzx // gyz
_r = abs(gyz // _z)

assert isPrime(_p) and isPrime(_r) and isPrime(_q)
assert magic(x, y, z) == magic(_p, _r, _q)

##############################
# Recover the signature of FLAG
##############################

f = magic(_p, _r, _q)
nb = (f.denominator.bit_length() + 7) // 8

d = int(pow(f.numerator, -1, prod([x - 1 for x in [_p, _r, _q]])))
mix = [pow(c, d, f.denominator) for c in mix]
mix = [(mix[0] + mix[1]) // 2, (mix[0] - mix[1]) // 2]

r = int(pow(mix[0], f.numerator, f.denominator))
c = int(pow(mix[1], f.numerator, f.denominator))
Mod = _p * _r * _q

##############################
# Find irreducible fraction by solving HNP
##############################

M = Matrix(ZZ, 2, 2)
M[0, 0] = r
M[1, 0] = Mod
M[0, 1] = 1

M = M.LLL()
_x, _y = int(M[0, 0]), int(M[0, 1])

##############################
# Brute-force all possibilities of (m^2 * c + h^2 * m + c^2 * h,  h * c * m)
##############################

P.<m> = PolynomialRing(ZZ)
for i in range(1, 2^12):
	x, y = i * _x, i * _y 			# x = m^2 c + h^2 m + c^2 h, y = hcm
	mh = y // c
	f = c * m^3 - x * m + (mh^2 + c^2 * mh)
	for _m in f.roots():
		FLAG = long_to_bytes(int(_m[0]))
		print(FLAG)
		sys.exit()
	
