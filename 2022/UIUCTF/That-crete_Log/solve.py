from Crypto.Util.number import *
from functools import reduce
from operator import mul
import random
from pwn import *

def gen():

	while True:
		nbits = random.randint(520, 620)
		p = getPrime(nbits)
		factors = [p, 2]

		while p.bit_length() < 1000:
			q = 0
			while True:
				kbits = random.randint(10, 16)
				q = getPrime(kbits)
				if q not in factors:
					break
			factors += [q]
			p *= q

			if isPrime(2 * p + 1):
				return 2 * p + 1, factors



r = remote("log.chal.uiuc.tf", 1337)
r.recvuntil("Here's your token for the session: ")
token = int(r.recvline().decode().strip())

mod = []
res = []

for _ in range(5):
	p, fs = gen()
	r.recvuntil("Give me the prime factors of phi(N): ")
	factors = " ".join([str(f) for f in fs])	
	r.sendline(factors)
	r.recvuntil("x = ")
	x = int(r.recvline().decode().strip())
	r.recvuntil("out = ")
	out = int(r.recvline().decode().strip())

	for f in fs[1:]:
		if f in mod:
			continue

		lift = (p - 1) // f

		_x = pow(x, lift, p)
		tmp = _x
		_out = pow(out, lift, p)

		for i in range(1, f + 1):
			if tmp == _out:
				mod += [f]	
				res += [i]
				break
			tmp *= _x
			tmp %= p

	print(mod)
	print(res)

x = 0
N = reduce(mul, mod)
	
for i, m in enumerate(mod):
		
	if m == 1:
		continue
	Ni = N // m
	x += res[i] * Ni * inverse(Ni, m)

msg = x % N
msg ^= token
print(long_to_bytes(msg))

print(N.bit_length())
