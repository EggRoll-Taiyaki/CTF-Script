from pwn import *
from json import loads, dumps

def conn():

	return remote("integral-communication.chal.irisc.tf", 10103)

def create_command(server, msg):
	
	server.sendlineafter(b">", b"1")
	server.sendlineafter(b"Please enter your message: ", b"aaaaa")
	server.recvuntil("IV: ")
	IV = bytes.fromhex(server.recvline().decode())
	server.recvuntil("Command: ")
	ct = bytes.fromhex(server.recvline().decode())

	return IV, ct

def run_command(server, IV, ct):

	server.sendlineafter(b">", b"2")
	server.sendlineafter(b"IV: ", IV.hex())
	server.sendlineafter(b"Command: ", ct.hex())

	return

def xor(a, b):

	return bytes([x ^ y for x, y in zip(a, b)])

def fake_command(server):

	"""
		tmp = {"from": "guest", "act": "echo", "msg": "aaaaa"}
		tmp = dumps(tmp).encode()
		assert len(tmp) % 16 == 0

		for i in range(len(tmp) // 16):
	 		print(tmp[16 * i: 16 * i + 16])

		b'{"from": "guest"'
		b', "act": "echo",'
		b' "msg": "aaaaa"}'
	"""

	IV, ct = create_command(server, b"aaaaa")
	ct = xor(ct[: 16], xor(b', "act": "echo",', b', "act": "flag",')) + ct[16: ]
	run_command(server, IV, ct)
	
	server.recvuntil(b"Failed to decode UTF-8: ")
	_ = bytes.fromhex(server.recvline().decode())
	IV = xor(IV, xor(_[:16], b'{"from": "admin"'))
	run_command(server, IV, ct)

	server.interactive()
	
server = conn()
fake_command(server)


