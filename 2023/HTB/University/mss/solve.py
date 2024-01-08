from pwn import *
import json
from Crypto.Util.number import *
from math import prod
from hashlib import sha256
from Crypto.Cipher import AES

def conn():

	return remote("83.136.250.104", 54040)

def get_share(s, x):

	payload = {"command": "get_share", "x": x}
	s.sendlineafter(b"- Exit", json.dumps(payload))
	_ = s.recvline()
	_ = s.recvline()
	_ = json.loads(s.recvline().decode().strip().split(" = ")[1])
	return int(_["y"])

def encrypt_flag(s):

	payload = {"command": "encrypt_flag"}
	s.sendlineafter(b"- Exit", json.dumps(payload))
	_ = s.recvline()
	_ = s.recvline()
	_ = s.recvline()
	_ = json.loads(s.recvline().decode().strip().split(" : ")[1][:-1])
	return _

def recover_key(s, max_num_of_shares, max_value_of_x):

	primes = []
	for i in range(max_value_of_x, -1, -1):
		if isPrime(i):
			primes += [i]
			if len(primes) == max_num_of_shares:
				break
	residues = []
	for p in primes:
		y = get_share(server, p)
		residues += [y % p]

	Mod = prod(primes)
	key = 0
	for p, r in zip(primes, residues):
		key += r * (Mod // p) * pow(Mod // p, -1, p)
		key %= Mod	

	return key

server = conn()
key = recover_key(server, 19, 2**15)
key = sha256(str(key).encode()).digest()
_ = encrypt_flag(server)
cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(_["iv"]))
FLAG = cipher.decrypt(bytes.fromhex(_["enc_flag"]))
print(FLAG)
