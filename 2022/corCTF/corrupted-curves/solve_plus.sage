from pwn import *
import random
from itertools import product

def conn():

	r = remote("be.ax", 31132)
	return r

def get_enc(r):

	r.recvuntil("p = ")
	p = int(r.recvline().decode().strip())
	r.recvuntil("flag y = ")
	fy = int(r.recvline().decode().strip())

	return p, fy

def get_data(r, n):

	e, x, y = [], [], []
	while len(x) < n:
		_ = r.recvline().decode().strip()
		if ":(" in _:
			r.recvuntil("more> ")
			r.sendline("yes")
			continue
		_e = int(_.split(" = ")[1])
		_ = r.recvline().decode().strip()
		if ":(" in _:
			r.recvuntil("more> ")
			r.sendline("yes")
			continue
		_x = int(_.split(" = ")[1])
		r.recvuntil("y = ")
		py = int(r.recvline().decode().strip())
		e += [_e]
		x += [_x]
		y += [py]

		r.recvuntil("more> ")
		r.sendline("yes")

	return e, x, y

r = conn()
p, fy = get_enc(r)
n = 500
e, x, y = get_data(r, n)
m = 48
ind1, ind2 = -1, -1
for i in range(n):
	for j in range(i+1, n):
		diff = bin(e[i] ^^ e[j])[2:].count("1")
		if diff < m:
			m = diff
			ind1, ind2 = i, j

print(m)

tmp = e[ind1] ^^ e[ind2]
delta = []
for i in range(48):
	if tmp & (1 << i):
		delta += [1 << i]			

k_list = []
for coef in product([-1, 1], repeat = m):
	k_list += [sum([coef[i] * delta[i] for i in range(m)])]

"""
	x1^3 + (a1) * x1 + (b1) = y1^2
	x2^3 + (a1 + k1) * x2 + (b1 + k2) = y2^2
	
	a1 * (x2 - x1) = (y2^2 - x2^3 - y1^2 + x1^3) - k1 * x2 - k2
"""

for k1 in k_list:
	for k2 in k_list:
		a = ((y[ind2]**2 - x[ind2]**3 - y[ind1]**2 + x[ind1]**3 - k1 * x[ind2] - k2) * pow(x[ind2] - x[ind1], -1, p)) % p 
		b = (y[ind1]**2 - x[ind1]**3 - a * x[ind1]) % p
		
		a = a ^^ e[ind1]
		b = b ^^ e[ind1]

		if a < (1 << 384) and b < (1 << 384):
			print(a)
			print(b)
			print(p)
			print(fy)
			
			P.<x> = PolynomialRing(Zmod(p))
			f = fy^2 - x^3 - a * x - b
			print(f.roots())
