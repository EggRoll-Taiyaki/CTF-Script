from pwn import *

def conn():

	r = remote("46.101.90.48", 30931)
	return r

def find_mod():

	lb, ub = 0, 2**256
	while lb < ub:
		x = (lb + ub) // 2
		r = conn()
		r.recvuntil(b"> ")
		r.sendline(b"1")
		r.recvuntil(b"x: ")
		r.sendline(str(x))
		_ = r.recvline().decode()
		if "Coordinate greater than curve modulus" in _:
			ub = x
		else:
			lb = x + 1
		r.close()
	return lb

def find_param(r, p):

	x = 0
	while True:
		r.recvuntil(b"> ")
		r.sendline(b"1")
		r.recvuntil(b"x: ")
		r.sendline(str(x))
		_ = r.recvline().decode().strip().split(", ")
		if "Point confirmed on curve" in _[0]:
			break
		x += 1	

	Px, Py = [], []
	for _ in range(2):
		r.recvuntil(b"> ")
		r.sendline(b"2")
		r.recvline()
		_ = r.recvline().decode().strip()[:-1].split(", ")
		Px += [int(_[1])]
		Py += [int(_[2])]
	
	### y^2 = x^3 + a * x + b (mod p)
	a = (pow(Px[0] - Px[1], -1, p) * ((Py[0]**2 - Px[0]**3) - (Py[1]**2 - Px[1]**3))) % p
	b = (Py[0]**2 - Px[0]**3 - a * Px[0]) % p

	for _ in range(10):
		r.recvuntil(b"> ")
		r.sendline(b"2")
		r.recvline()
		_ = r.recvline().decode().strip()[:-1].split(", ")
		x, y = int(_[1]), int(_[2])
		assert (y**2 - x**3 - a * x - b) % p == 0

	return a, b

def a0(P, Q): 
	if P[2] == 0 or Q[2] == 0 or P == -Q: 
		return 0 
	if P == Q: 
		a = P.curve().a4() 
		return (3*P[0]^2+a)/(2*P[1]) 
	return (P[1]-Q[1])/(P[0]-Q[0]) 

def add_augmented(PP, QQ):
	(P, u), (Q, v) = PP, QQ
	return [P+Q, u + v + a0(P,Q)]

def scalar_mult(n, PP):
	t = n.nbits()
	TT = PP.copy()
	for i in range(1,t):
		bit = (n >> (t-i-1)) & 1
		TT = add_augmented(TT, TT)
		if bit == 1:
			TT = add_augmented(TT, PP)
	return TT

def solve_ecdlp(P,Q,p):
	R1, alpha = scalar_mult(p, [P,0])
	R2, beta  = scalar_mult(p, [Q,0])
	return ZZ(beta*alpha^(-1))

def predict(r, p, a, b):

	Px, Py = None, None
	r.recvuntil(b"> ")
	r.sendline(b"2")
	r.recvline()
	_ = r.recvline().decode().strip()[:-1].split(", ")
	Px, Py = int(_[1]), int(_[2])

	E = EllipticCurve(GF(p), [a, b])

	G = E.lift_x(4)
	P = E(Px, Py)

	n = solve_ecdlp(G, P, p)
	seed = Mod(n, p).sqrt()
	print(pow(seed, 2, p))
	print(n)

	inc = int.from_bytes(b'Coordinates lost in space', 'big')
	next_seed = (a * pow(seed, 3) + b * seed + inc) % p
	next_P = G * seed * next_seed
	
	r.recvuntil(b"> ")
	r.sendline(b"3")
	r.sendlineafter(b"x: ", str(next_P[0]))
	r.sendlineafter(b"y: ", str(next_P[1]))
	r.interactive()

# p = find_mod()
p = 91720173941422125335466921700213991383508377854521057423162397714341988797837
r = conn()
# a, b = find_param(r, p)
a = 57186237363769678415558546920636910250184560730836527033755705455333464722170
b = 47572366756434660406002599832623767973471965640106574131304711893212728437629
# setup
r.recvuntil(b"> ")
r.sendline(b"1")
r.recvuntil(b"x: ")
r.sendline(b"4")
predict(r, p, a, b)
