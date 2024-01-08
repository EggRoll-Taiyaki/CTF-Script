from output import *
from decimal import *
from Crypto.Util.number import *
import sys

##############################
# Recover the values of k, l
##############################

getcontext().prec = int(3000)

nbits = 2048
delta = 1/4
i = int(nbits * delta)

kl = int((2^(2*i) * e^2 * dp * dq // N) + 1)
for q in range(2):
	s = int(int((1 - kl * (N - 1)) % e) + q * e)
	D = int( Decimal(int(s^2 - 4 * kl)) ** (Decimal(int(1))/Decimal(int(2))) )
	k, l = int((s + D) // 2), int((s - D) // 2)
	if k * l == kl:
		a = int((e * dp * 2**i + k - 1) * pow(e, -1, k * N))
		b = int((e * dp * 2**i + l - 1) * pow(e, -1, l * N))
		break

##############################
# Some hyper-params for LLL
##############################

m = 20
t = 10

R.<x> = PolynomialRing(ZZ)
f = x + a

X = 2^512

##############################
# Generate shift polynomials so that dp_L is root of them mod kp 
##############################

F, S = [], []
for i in range(m + 1):
	h = f^i * k^(m-i) * N^(max(0,t-i))
	F.append(h)
	S.append(x^i)

##############################
# Put coefficients of shift polynomials in matrix
##############################

MAT = Matrix(ZZ, len(F))

for i in range(len(F)):
	f = F[i]
	f = f(x*X)

	coeffs = (f.coefficients(sparse=False))
	for j in range(len(coeffs), len(F)):
		coeffs.append(0)
	coeffs = vector(coeffs)
	MAT[i] = coeffs

##############################
# Standard LLL
##############################

MAT = MAT.LLL()

##############################
# Form polynomials from short vectors
##############################

for j in range(len(F)):
	_f = 0
	for i in range(len(S)):
		cij = MAT[j, i]
		cij = cij / S[i](X)
		cj = ZZ(cij)
		_f = _f + cj * S[i]

	for (r, _) in _f.roots():
		if gcd(r + a, N) != 1:
			p = gcd(r + a, N)
			q = N // p
			d = int(pow(e, -1, (p-1) * (q-1)))
			FLAG = long_to_bytes(pow(c, d, N))
			print(FLAG)
			sys.exit()		

