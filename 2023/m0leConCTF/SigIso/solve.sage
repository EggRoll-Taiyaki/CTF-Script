from pwn import *
import random
import string
import hashlib
import json

ls = list(prime_range(3, 117))
p = 4 * prod(ls) - 1
base = 0
N = len(ls)
T = 30
B = 5

R.<t> = GF(p)[]

#Thanks to Lorenz Panny @yx7 for the CSIDH code! :D
def montgomery_coefficient(E):
	a,b = E.short_weierstrass_model().a_invariants()[-2:]
	r, = (t**3 + a*t + b).roots(multiplicities=False)
	s = sqrt(3*r**2 + a)
	return -3 * (-1)**is_square(s) * r / s

def csidh(pub, priv):
	E = EllipticCurve(GF(p), [0, int(pub), 0, 1, 0])
	assert (p+1) * E.random_point() == E(0)
	for es in ([max(0,+e) for e in priv], [max(0,-e) for e in priv]):
		while any(es):
			x = GF(p).random_element()
			try: P = E.lift_x(x)
			except ValueError: continue
			k = prod(l for l,e in zip(ls,es) if e)
			P *= (p+1) // k
			for i,(l,e) in enumerate(zip(ls,es)):
				if not e: continue
				k //= l
				Q = k*P
				if Q == 0: continue
				phi = E.isogeny(Q)
				E,P = phi.codomain(), phi(P)
				es[i] -= 1
		E = E.quadratic_twist()
	return int(montgomery_coefficient(E))

def conn():

	r = remote("sigiso.challs.m0lecon.it", 8888)
	
	### PoW
	r.recvuntil(b"Give me a string starting in ")
	_ = r.recvline().decode().strip()[:-1].split(" such that its sha256sum ends in ")
	while True:
		s = _[0] + "".join([random.choice(string.ascii_letters) for i in range(10)])
		if hashlib.sha256(s.encode()).hexdigest().endswith(_[1]):
			r.sendline(s)
			return r

def sign(r, msg):
	
	# assert msg.isalnum()
	# assert "flag" not in msg.lower()
	r.sendlineafter(b"> ", b"1")
	r.sendlineafter(b"What's your message?", msg)
	r.recvline()
	return json.loads(r.recvline())["signature"]

def recover_sk(r):

	r.recvuntil(b"Server's public key is: ")
	pk = int(r.recvline().decode().strip())

	sk = [-B for i in range(N)]
	cnt = 0
	threshold = 2 * B

	while True:
		msg = "".join([random.choice(string.digits) for i in range(20)])
		sigma = sign(r, msg.encode())
		for sig in sigma:
			if sig["bit"] == 0:
				continue
			for i, v in enumerate(sig["vec"]): 
				# sk[i] = fs[?][i] - v
				# 3 -> -8 ~ 2
				sk[i] = max(sk[i], -B - v)
			cnt += 1
		if cnt >= threshold:
			if pk == csidh(base, sk):
				return sk
			cnt = 0

def sub(a, b):
	return [x-y for x,y in zip(a, b)]

def forge(msg, sk):

	fs = []
	Es = []
	for i in range(T):
		f = [random.randint(-B, B) for _ in range(N)]
		E = csidh(base, f)
		fs.append(f)
		Es.append(E)
	s = ",".join(map(str, Es)) + "," + msg
	h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
	outs = []
	for i in range(T):
		b = (h>>i) & 1
		if b:
			outs.append({"bit": int(b), "vec": [int(x) for x in sub(fs[i], sk)]})
		else:
			outs.append({"bit": int(b), "vec": [int(x) for x in fs[i]]})
	return outs

r = conn()
sk = recover_sk(r)
outs = forge("gimmetheflag", sk)
r.sendlineafter(b"> ", b"2")
r.sendline(json.dumps({"msg": "gimmetheflag", "signature": outs}))
r.interactive()
