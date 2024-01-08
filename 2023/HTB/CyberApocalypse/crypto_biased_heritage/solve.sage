from pwn import *
import os
from hashlib import sha256
from Crypto.Util.number import isPrime, getPrime, long_to_bytes, bytes_to_long

def conn():

	r = remote("165.232.108.200", 32542)	
	return r

def get_param(r):

	r.recvuntil(b"g:")
	g = int(r.recvline())
	r.recvuntil(b"y:")
	y = int(r.recvline())
	r.recvuntil(b"p:")
	p = int(r.recvline())

	return g, y, p

def sign(r, msg):

	r.recvuntil(b"> ")
	r.sendline(b"S")
	r.recvuntil(b"Enter message> ")
	r.sendline(msg.hex())
	r.recvuntil(b"Signature:")
	_ = r.recvline().decode().split(", ")
	
	return int(_[0][2:]), int(_[1][:-2])

def hnp(t, u, n, k):

	L = len(t)
	M = Matrix(RationalField(), L+1, L+1)
	for i in range(L):
		M[i, i] = n
		M[L, i] = t[i]
	M[L, L] = 1 / (2 ** (k + 1))

	def babai(A, w):
		C = max(max(row) for row in A.rows())
		B = matrix([list(row) + [0] for row in A.rows()] + [list(w) + [C]])
		B = B.LLL(delta=0.9)
		return w - vector(B.rows()[-1][:-1])

	closest = babai(M, vector(u + [0]))
	return (closest[-1] * (2 ** (k + 1))) % n

def recover_privkey(r, q, y):

	inv = int(pow(2**256 + 1, -1, q))

	s, e = [], []
	for _ in range(2):
		msg = os.urandom(16)	
		_s, _e = sign(r, msg)
		s += [int(- _s * inv % q)]
		e += [int(_e * inv % q)]

	### x * e = k - s (mod q)
	"""
	M = Matrix(QQ, [
		[QQ(q), 0, 0, 0],
		[0, QQ(q), 0, 0],
		[QQ(e[0]), QQ(e[1]), QQ(B) / QQ(q), 0],
		[QQ(s[0]), QQ(s[1]), 0, QQ(B)]
	])

	M = M.LLL()
	for row in M:
		if abs(row[-1]) == B:
			k = row[-1] // B
			x = int(QQ(-k * row[-2]) * q / B) % q
			print(pow(g, x, p))
	"""
	x = int(hnp(e, s, q, 256))

	return x

def H(msg):
	return int(bytes_to_long(2 * sha256(msg).digest()) % q)

r = conn()
g, y, p = get_param(r)
q = (p - 1) // 2
r.close()
while True:
	r = conn()
	x = recover_privkey(r, q, y)
	# forge sig
	msg = b"right hand"
	k = H(msg + long_to_bytes(x))
	tmp = pow(g, k, p) % q
	e = H(long_to_bytes(tmp) + msg)
	s = (k - x * e) % q
	# get flag
	r.recvuntil(b"> ")
	r.sendline(b"V")
	r.sendlineafter(b"Enter message> ", msg.hex())
	r.sendlineafter(b"Enter s> ", str(s))
	r.sendlineafter(b"Enter e> ", str(e))
	_ = r.recvline()
	if b"HTB" in _:
		print(_)
		break
	r.close()
