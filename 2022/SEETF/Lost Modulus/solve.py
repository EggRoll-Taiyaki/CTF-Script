from pwn import *
import os
from Crypto.Util.number import *
from decimal import *

getcontext().prec = 1000

def conn():
	
	r = remote("fun.chall.seetf.sg", 30004)
	return r

def get_multiple(r):

	m1 = bytes_to_long(b"SEE{" + os.urandom(200))
	m2 = int(Decimal(m1) ** (Decimal(1) / Decimal(3)))
	m1 = m2 ** 3

	r.sendlineafter("Message 1 (as integer) : ", str(m1))
	r.sendlineafter("Message 2 (as integer) : ", str(m2))

	r.recvline()
	r.recvline()	
	_ = r.recvline().decode().strip()[1:-1].split(",")
	c1, c2 = int(_[0]), int(_[1])
	return (c2 ** 3) - c1


r = conn()
n = get_multiple(r)
r.close()
for _ in range(10):
	r = conn()
	n = GCD(n, get_multiple(r))
	r.close()

print(n)


