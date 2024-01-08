from pwn import *
import json
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

def conn():

	r = remote("165.232.98.59", 30207)
	return r

def get_param(r):

	r.recvline(b"This is the point you calculated before:")
	_ = json.loads(r.recvline())
	x, y = int(_["x"], 16), int(_["y"], 16)
	
	p, a, b = 0, 0, 0
	for _ in range(256):
		r.sendlineafter(b"> ", b"1")
		_ = json.loads(r.recvline())
		p, a, b = int(_["p"], 16), max(int(_["a"], 16), a), max(int(_["b"], 16), b)

	r.sendlineafter(b"> ", b"2")
	_ = json.loads(r.recvline())
	iv, enc = bytes.fromhex(_["iv"]), bytes.fromhex(_["enc"])

	return x, y, p, a, b, iv, enc

r = conn()
x, y, p, a, b, iv, enc = get_param(r)
lift = 512 // 3
approx = int((y**2 - x**3 - (a << lift) * x - (b << lift)) % p)
M = Matrix(ZZ, [
	[p, 0, 0],
	[x, 1, 0],
	[approx, 0, 2**lift]
])
M = M.LLL()
for row in M:
	if abs(row[-1]) == 2**lift:
		LSB_a = int((row[-2] * (- row[-1] // 2**lift)) % p)
		a = (a << lift) + LSB_a
		b = int((y**2 - x**3 - a * x) % p)
		key = sha256(long_to_bytes(int(pow(a, b, p)))).digest()[:16]
		cipher = AES.new(key, AES.MODE_CBC, iv)
		print(cipher.decrypt(enc))
