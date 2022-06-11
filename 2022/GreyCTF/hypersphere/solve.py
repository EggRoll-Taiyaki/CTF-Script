from Crypto.Util.number import *
import random
import point
from functools import reduce
from operator import mul
from hashlib import shake_256

def decrypt(enc : bytes, key : str):
	otp = shake_256(key.encode()).digest(len(enc))
	return xor(otp, enc)

def xor(a : bytes, b : bytes):
	return bytes([ x ^ y for x, y in zip(a, b)])

def gen_smooth_prime(nbits, fbits):

	while True:
		n = 2
		prime_list = []

		while n.bit_length() < nbits:
			prime = getPrime(fbits)
			while prime in prime_list:
				prime = getPrime(fbits)
			n *= prime
			prime_list += [prime]

		p = n + 1

		if isPrime(p) and p % 4 == 3:
			return p, prime_list

def random_point(p):

	a = random.randint(0, p - 1)
	b = random.randint(0, p - 1)

	while True:
		c = random.randint(0, p - 1)
		dd = (1 - a * a - b * b - c * c) % p
		d = pow(dd, (p + 1) // 4, p)

		if pow(d, 2, p) == dd:
			return point.Point(a, b, c, d, p)

def gen_good_point(p, prime_list):

	while True:

		g = random_point(p)
		g = g ** (p * (p + 1))

		if 10 < g.a < p - 2 and 10 < g.b < p - 2 and 10 < g.c < p - 2 and 10 < g.d < p - 2:
			break

	check = False

	while check == False:

		check = True

		for pf in prime_list:

			lift = (p - 1) // pf
			test = g ** lift
			if test.a == 1 and test.b == 0 and test.c == 0 and test.d == 0:
				check = False

	return g

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
	
def dlog(p, prime_list, g, A):

	res = []

	for pf in prime_list:
				
		lift = (p - 1) // pf
		lift_g = g ** lift	
		lift_A = A ** lift

		x = lift_g

		for i in range(1, pf + 1):
	
			if x.a == lift_A.a and x.b == lift_A.b and x.c == lift_A.c and x.d == lift_A.d:
				res += [i]
				break
			x *= lift_g
		
	return crt(res, prime_list)

print("Generating ...")

p, prime_list = gen_smooth_prime(600, 16)
print(f"p = {p}")

g = gen_good_point(p, prime_list)
print(f"g = {g.a} {g.b} {g.c} {g.d}")

# a = random.getrandbits(512)
# A = g ** a

_ = input("A = ").split(", ")
A = point.Point(int(_[0]), int(_[1]), int(_[2]), int(_[3]), p)
_ = input("B = ").split(", ")
B = point.Point(int(_[0]), int(_[1]), int(_[2]), int(_[3]), p)
b = dlog(p, prime_list, g, B)
S = A ** b
key = str(S)

enc = bytes.fromhex(input("c = "))
msg = decrypt(enc, key)
print(f"msg = {msg}")


