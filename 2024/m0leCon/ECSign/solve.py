from Crypto.PublicKey.ECC import EccPoint
import hashlib
import json
from pwn import *
import string
import random

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = EccPoint(Gx, Gy)

N = 32
T = 64
B = 4

def conn():

	return remote("ecsign.challs.m0lecon.it", 6482)

def get_pk(s):

	_ = s.recvline().decode().strip()[1:-1].split(", ")
	bases = [int(b) for b in _]

	_ = s.recvline().decode().strip().split(" ")
	Px, Py = [int(z) for z in _]

	return bases, (Px, Py)

def choice(s, ch):

	s.sendlineafter(b">", ch)

def sign(s, m):

	choice(s, b"1")
	s.sendlineafter(b"The message to sign: ", m)
	return json.loads(s.recvline())

def recover_sk(s):

	sk = [None for _ in range(N)]
	for _ in range(T * B * (3 * B)):
		m = "".join([random.choice(string.ascii_letters) for _ in range(30)])
		sigs = sign(s, m.encode())
		for sig in sigs:
			b, fs = sig
			if b:
				continue
			for i in range(N):
				if fs[i] < -N*T*B:
					if sk[i]:
						sk[i] = min(sk[i], fs[i] + N*T*B)
					else:
						sk[i] = fs[i] + N*T*B
				if fs[i] > N*T*B:
					if sk[i]:
						sk[i] = max(sk[i], fs[i] - N*T*B)
					else:
						sk[i] = fs[i] - N*T*B
		if _ % T == 0:
			print(sk)
	sk = [x if x else 0 for x in sk]
	return sk					

def sub(a, b):
	return [x-y for x,y in zip(a, b)]

def action(pub, priv):
	res = 1
	for li, ei in zip(bases, priv):
		res = (res * pow(li, ei, q)) % q
	Q = res * pub
	return Q

server = conn()
server.recvline()
bases, P = get_pk(server)
sk = recover_sk(server)
# validation
print(action(G, sk).x, action(G, sk).y)
print(P)
fs = []
Ps = []
cnt = 0
while cnt < T:
	f = [random.randint(-(N*T+1)*B, (N*T+1)*B) for _ in range(N)]
	b = sub(f, sk)
	vec = [-N*T*B <= bb <= N*T*B for bb in b]
	if all(vec):
		P = action(G, f)
		fs.append(f)
		Ps.append((P.x,P.y))
		cnt += 1
s = ",".join(map(str, Ps)) + "," + "gimmetheflag"
h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
outs = []
for i in range(T):
	b = (h>>i) & 1
	if b:
		outs.append((b, sub(fs[i], sk)))
	else:
		outs.append((b, fs[i]))
choice(server, b"2")
server.sendlineafter(b"Give me a valid signature: ", json.dumps(outs))
server.interactive()
