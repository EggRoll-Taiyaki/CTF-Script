from pwn import *
from Crypto.Util.number import *
from itertools import product
import random

# Fill in the connection info
IP = "172.25.9.4"
PORT = 9999

def conn():

	return remote(IP, PORT)

def oracle(server, ct):

	server.sendlineafter(b"give me your message to decrypt\n> ", hex(ct).encode())
	return int(server.recvline(), 16)

def luck():

	server = conn()

	"""
		Retrieve parameters for the chall
	"""
	server.recvuntil(b"n=\n")
	n = int(server.recvline(), 16)
	print(f"{n=}")	

	server.recvuntil(b"your token is\n")
	c = int(server.recvline(), 16)
	e = 0x10001
	print(f"{c=}")

	inv = pow(2, -20, n)
	M = [oracle(server, (pow(inv, i * e, n) * c) % n) for i in range(100)]

	LSB_list = []
	cnt = 1
	for i in range(50):
		ks = []
		for k in range(2**20):
			if ((M[i] + k * n) >> 512) % 2**20 == (M[i+1] >> 492) % 2**20:
				ks += [k]
		
		LSB_list += [[(-k * n) % 2**20 for k in ks]]
		cnt *= len(LSB_list[-1])

		if cnt > 2**16:
			server.close()
			print("Too many possibilities!")
			return
	print(cnt)
	
	for LSB in product(*LSB_list):
		token, cur = 0, 0
		for i in range(50):
			t = (LSB[i] - (inv * cur) % n) % 2**20
			cur = (inv * cur + t) % n 
			token = 2**(20 * i) * t + token
		if pow(token, e, n) == c:
			print("Found!")
			server.sendlineafter(b"give me your token\n> ", hex(token)[2:].encode())
			print(server.recvline())
			break

	server.close()

for _ in range(100):
	try:
		luck()
	except:
		pass
