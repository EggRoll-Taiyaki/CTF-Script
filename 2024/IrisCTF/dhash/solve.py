from pwn import *
import os
from Crypto.Util.number import *

def conn():

	return remote("dhash.chal.irisc.tf", 10101)

def get_N(server):

	server.recvuntil(b"MySeededHash")
	_ = server.recvline().decode().split(", ")
	N, e = int(_[0][1:]), int(_[1][:-2])

	return N, e

def xor(a, b):

	return bytes(x^y for x,y in zip(a,b))

def fake(N, e):

	blocks = [bytes_to_long(os.urandom(128)).to_bytes(256, "big") for _ in range(2)]
	tmp = [pow(bytes_to_long(block), e, N).to_bytes(256, "big") for block in blocks]
	blocks += [pow(bytes_to_long(xor(tmp[0], tmp[1])), pow(e, -1, N-1), N).to_bytes(256, "big")]
	
	return b"".join(blocks)
	

server = conn()
N, e = get_N(server)
preimage = fake(N, e)
server.sendlineafter(b"> ", preimage.hex())
server.interactive()

