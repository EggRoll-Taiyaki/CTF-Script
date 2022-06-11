from out import *
from Crypto.Util.number import *
from functools import reduce
from operator import mul

def to_cycles(perm):

	n = len(perm)
	
	ind = [i for i in range(n)]
	cycles = []

	while len(ind) > 0:
		cycle = [ind[0]]
		ind.pop(0)
		while True:
			next = perm[cycle[-1]]
			if next == cycle[0]:
				break
			cycle += [next]
			ind.remove(next)
		cycles += [cycle]

	return cycles

def dlog(perm_g, perm_A):

	g_cycles = to_cycles(perm_g)

	res, mod = [], []

	for g_cycle in g_cycles:
		ord = g_cycle.index(perm_A[g_cycle[0]])

		res += [ord]
		mod += [len(g_cycle)]

	return crt(res, mod)

def crt(res, mod):

	### Fake CRT, it works only when modules are pairwise relatively coprime

	x = 0

	N = reduce(mul, mod)
	for i, m in enumerate(mod):
		if m == 1:
			continue
		Ni = N // m
		x += res[i] * Ni * inverse(Ni, m)

	return x % N

a = dlog(g, A)
a = 1530077333743

# b = dlog(g, B)
# print(b)

from hashlib import shake_256
import perm

_B = perm.Perm(B)
_S = _B ** a
key = str(_S)

def decrypt(key : str, ct : bytes) -> str:
	otp = shake_256(key.encode()).digest(len(ct))
	return xor(otp, ct)

def xor(a : bytes, b : bytes) -> bytes:
	return bytes([ x ^ y for x, y in zip(a, b)])

FLAG = decrypt(key, c)
print(FLAG)
