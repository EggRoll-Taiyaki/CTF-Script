import json
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import *

from pwn import remote
from math import prod

while True:
	P, ps = 1, []
	while P < 2**1024:
		p = getPrime(16)
		if p not in ps:
			P *= p
			ps += [p]
	if isPrime(P + 1):
		n = P + 1
		break

def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

def sample(start, N):
    while jacobi(start, N) != 1:
        start += 1
    return start

def checker(x, ps):
    return all(jacobi(x, p) == 1 for p in ps)

server = remote("yaot.challs.m0lecon.it", 2844)
server.sendlineafter(b"Send me a number: ", str(n).encode())

phi = prod([p - 1 for p in ps])
d_n = pow(n, -1, phi)
tts = json.loads(conn.recvline())["vals"]
ts = [pow(tt, d_n, n) for tt in tts]
assert [pow(t, n, n) for t in ts] == tts

for _ in range(128):
	data = json.loads(conn.recvline())
	c0, c1 = data["c0"], data["c1"]
	m0 = int(not checker(c0, ps))
	m1 = int(not checker(c1, ps))
	server.sendline(json.dumps(
		{
			"m0": m0,
			"m1": m1
		}
	).encode())

ct = bytes.fromhex(conn.recvline().decode())
key = sha256((",".join(map(str, ts))).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
pt = unpad(cipher.decrypt(ct), 16)
print(pt)

