from pwn import *
import string
from itertools import product
from hashlib import sha256, sha512, md5
from Crypto.Util.number import *

alphabet = string.ascii_letters + string.digits

def conn():

	r = remote("1.13.154.182", 30032)
	return r

def proof_of_work(r):

	r.recvuntil("sha256(XXXX+")
	_ = r.recvline().decode().strip().split(") == ")
	for (X1, X2, X3, X4) in product(alphabet, repeat = 4):
		s = X1 + X2 + X3 + X4 + _[0]
		if sha256(s.encode()).hexdigest() == _[1]:
			r.sendline(s[:4])
			return

def determinant(row1, row2, row3):

	return (row1[0] * (row2[1] * row3[2] - row2[2] * row3[1]) \
		- row1[1] * (row2[0] * row3[2] - row2[2] * row3[0]) \
		+ row1[2] * (row2[0] * row3[1] - row2[1] * row3[0]))

def intercept_and_recover(r):

	USER_NUM = 5
	users = [chr(ord("A") + i) for i in range(26)]

	rows = []

	for username in users:
		r.recvuntil("Input your choice please: ")
		r.sendline("R")
		r.recvuntil("Input your name: ")
		r.sendline(username)
		_ = r.recvline()

		if b"Registration success, keep your account well!" in _:
			r.recvuntil("e, d, h1, h2 = (")
			_ = r.recvline().decode().strip()[:-1].split(", ")
			e, d, h1, h2 = int(_[0]), int(_[1]), int(_[2]), int(_[3])
			rows += [[d * h1, d * h2, 1]]
	
		if len(rows) >= USER_NUM:
			break

	zq = determinant(rows[0], rows[1], rows[2])
	for i in range(USER_NUM):
		for j in range(i+1, USER_NUM):
			for k in range(j+1, USER_NUM):
				zq = GCD(zq, determinant(rows[i], rows[j], rows[k]))

	s1p = pow(rows[1][1] * rows[0][0] - rows[0][1] * rows[1][0], -1, zq) * (rows[1][1] - rows[0][1]) % zq
	s2p = (1 - rows[0][0] * s1p) * pow(rows[0][1], -1, zq) % zq

	r.recvuntil("Input your choice please: ")
	r.sendline("I")
	_ = r.recvline().decode().strip().split(" sent by ")

	cipher = _[0].split("message ")[1].split(", ")
	informant = _[1].split("...")[0]

	c1, c2 = int(cipher[0][1:]), int(cipher[1][:-1])

	h1 = int(sha256(informant.encode()).hexdigest(), 16)
	h2 = int(sha512(informant.encode()).hexdigest(), 16)

	d = pow(h1 * s1p + h2 * s2p, -1, zq)

	return informant, c1, c2, d

def get_flag(r, informant, c1, c2, d, N):

	F = pow(c2, d, N)
	m = int(md5(str(F).encode()).hexdigest(), 16) ^ c1

	r.recvuntil("Input your choice please: ")
	r.sendline("G")
	r.recvuntil("Input right messages in HEX and you\'ll get your bonus: ")
	r.sendline(hex(m)[2:])
	r.interactive()

r = conn()
proof_of_work(r)
r.recvuntil("Input your choice please: ")
r.sendline("P")
r.recvuntil("Here gives you some params about the KGC: ")
N = int(r.recvline().decode().split(", ")[0])
informant, c1, c2, d = intercept_and_recover(r)
get_flag(r, informant, c1, c2, d, N)
