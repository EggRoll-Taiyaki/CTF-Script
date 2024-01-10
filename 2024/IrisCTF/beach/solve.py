from pwn import *
import ast 
from util import *

local = False

def conn():

	if local:
		return process("./chal.py")
	else:
		return remote("beach.chal.irisc.tf", 10106)

def get_matrix(server):

	server.recvuntil(b"=")
	server.recvline()
	_ = server.recvline().decode().strip()
	m = ast.literal_eval(_)
	return m

def get_pub(server):

	X, Y, A_pub, B_pub = [get_matrix(server) for _ in range(4)]
	return X, Y, A_pub, B_pub

server = conn()
server.recvuntil(b"Computing keys")
X, Y, A_pub, B_pub = get_pub(server)
Xt1, Yt2, shift = luck_test(X, Y, A_pub, B_pub, 20)
K_b = pair_mul_mat([[(e[0]+shift, e[1]+shift) for e in c] for c in Xt1], pair_mul_mat(B_pub, Yt2))
h = hashlib.sha256(repr(K_b).encode()).hexdigest()
server.sendlineafter(b"What's my hash? ", h)
server.interactive()
