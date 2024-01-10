# https://en.wikipedia.org/wiki/Salsa20#ChaCha20_adoption

from Crypto.Util.number import long_to_bytes, bytes_to_long
import secrets
from pwn import *

def ROTL(a, b):
	return (((a) << (b)) | ((a % 2**32) >> (32 - (b)))) % 2**32

def qr(x, a, b, c, d):
	x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d],16)
	x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b],12)
	x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d], 8)
	x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b], 7)

ROUNDS = 20

def chacha_block(inp):
	x = list(inp)
	for i in range(0, ROUNDS, 2):
		qr(x, 0, 4, 8, 12)
		qr(x, 1, 5, 9, 13)
		qr(x, 2, 6, 10, 14)
		qr(x, 3, 7, 11, 15)

		qr(x, 0, 5, 10, 15)
		qr(x, 1, 6, 11, 12)
		qr(x, 2, 7, 8, 13)
		qr(x, 3, 4, 9, 14)

	return [(a+b) % 2**32 for a, b in zip(x, inp)]

def decrypt(data, prev_state):

	state = chacha_block(prev_state)
	buffer = b""
	output = []
	for b in data:
		if len(buffer) == 0:
			buffer = b"".join(long_to_bytes(x).rjust(4, b"\x00") for x in state)
			state = chacha_block(state)
		output.append(b ^ buffer[0])
		buffer = buffer[1:]
	return bytes(output)

def conn():
	
	return remote("babycha.chal.irisc.tf", 10100)

def xor(a, b):

	return bytes([x ^ y for x, y in zip(a, b)])

server = conn()
server.sendlineafter(b"> ", b"1")
server.sendlineafter(b"? ", b"0" * 64)
prev_buffer = xor(bytes.fromhex(server.recvline().decode()), b"0" * 64)
prev_state = [bytes_to_long(prev_buffer[4 * i: 4 * i + 4]) for i in range(16)]
server.sendlineafter(b"> ", b"2")
flag = decrypt(bytes.fromhex(server.recvline().decode()), prev_state)
print(flag)
