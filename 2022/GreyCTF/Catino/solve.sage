load('coppersmith.sage')

from random import getrandbits
from decimal import *

getcontext().prec = 6000

def generate(nbits, ind, leak):

	n = Decimal(getrandbits(nbits))
	p = Decimal(float(0.25))
	_ = str(n ** p).split(".")
	
	m_int = int(_[0] + _[1][:ind])
	m_float = int(_[1][ind: ind + leak])

	return n, m_int, m_float

def get_approx(nbits, ind, leak):

	n, m_int, m_float = generate(nbits, ind, leak)

	_ = m_int * 10**leak + m_float + 1
	r = str(_ ** 4).split("0" * 200)[-1]
	r = str(int(r)) # remove leading zeros
	
	return len(str(m_int)), len(r)

"""
	a = m_int * 10^leak
	b = m_float + 1

	c = 4a^3b + 6a^2b^2 + 4ab^3 + b^4 (mod 10^(4*leak)) is small

	Construct the following matrix

	4a^3b		c	0	0	0
	6a^3b^2		0	ac	0	0
	4a^3b^3		0	0	a^2c	0
	a^3b^4		0	0	0	a^3c
	10^(4*leak)a^3	0	0	0	0

	It contains a short vector (ac, a^3, a^3, a^3, a^3)
"""

def recover_m_int(approx, m_float, leak):

	a = 10^approx[0]
	b = m_float + 1
	c = 10^approx[1]

	M = [
		[4 * 10^(3 * leak) * a^3 * b^1, c, 0,		0,		0],
		[6 * 10^(2 * leak) * a^3 * b^2, 0, a * c,	0,		0],
		[4 * 10^(1 * leak) * a^3 * b^3, 0, 0, 		a^2 * c,	0],
		[1 * 10^(0 * leak) * a^3 * b^4, 0, 0, 		0,	  a^3 * c],
		[1 * 10^(4 * leak) * a^3 * b^0, 0, 0, 		0,		0]
	]

	M = Matrix(ZZ, M)
	L = M.LLL()

	return abs(int(L[0][3] // (a^2 * c)))

from pwn import *

def conn():

	r = remote("challs.nusgreyhats.org", 10520)
	return r

def collect_output(r, ROUND = 5):

	r.recvuntil("Generation complete!")
	
	res = []

	for i in range(ROUND):
		r.recvuntil("Guess the number (0-9): ")
		r.sendline(b"1")
		r.recvuntil("it was ")
		digit = r.recvline().decode().strip()
		res += [digit]

	return res

r = conn()
print("Waiting Server ...")
res = collect_output(r, 3000)
print("Finish Sampling ...")
m_float = int("".join(res))
print("Start Recovering")
m_int = recover_m_int([254, 9763], m_float, 3000)

fake_n = ((m_int * 10^3000) + m_float + 1)^4
n = int(str(fake_n).split("0" * 200)[0])

p = Decimal(float(0.25))
k = str(Decimal(n) ** p).split('.')[1]
randarr = list(k)
for i in range(3100, 3200):
	r.recvuntil("Guess the number (0-9): ")
	r.sendline(k[i])
r.interactive()
r.close()



