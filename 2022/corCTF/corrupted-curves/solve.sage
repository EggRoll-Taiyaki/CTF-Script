from pwn import *
import random

def conn():

	r = remote("be.ax", 31345)
	return r

def get_enc(r):

	r.recvuntil("p = ")
	p = int(r.recvline().decode().strip())
	r.recvuntil("flag y = ")
	fy = int(r.recvline().decode().strip())

	return p, fy

def get_multipliers(r, p):

	m, e, y, approx = [], [], [], []
	for i in range(1000):
		r.recvuntil("x = ")
		x = random.randint(2**384, 2**400)
		r.sendline(str(x))
		r.recvuntil("e = ")
		_e = int(r.recvline().decode().strip())
		_ = r.recvline().decode().strip()
		if "y" in _:
			py = int(_.split(" = ")[1])
			ma = int((py**2 - x**3) % p)
			approx += [ma]
			m += [x]
			e += [_e]
			y += [py]
			if len(m) == 64:
				break

	return m, e, y, approx

def build_basis(oracle_inputs, p):
    """Returns a basis using the HNP game parameters and inputs to our oracle
    """
    basis_vectors, d = [], len(oracle_inputs)
    for i in range(d):
        p_vector = [0] * (d+1)
        p_vector[i] = p
        basis_vectors.append(p_vector)
    basis_vectors.append(list(oracle_inputs) + [QQ(1)/QQ(p)])
    return Matrix(QQ, basis_vectors)

def approximate_closest_vector(basis, v):
    """Returns an approximate CVP solution using Babai's nearest plane algorithm.
    """
    BL = basis.LLL()
    G, _ = BL.gram_schmidt()
    _, n = BL.dimensions()
    small = vector(ZZ, v)
    for i in reversed(range(n)):
        c = QQ(small * G[i]) / QQ(G[i] * G[i])
        c = c.round()
        small -= BL[i] * c
    return (v - small).coefficients()

r = conn()
p, fy = get_enc(r)
m, e, y, approx = get_multipliers(r, p)

lattice = build_basis(m, p)
u = vector(ZZ, list(approx) + [0])
v = approximate_closest_vector(lattice, u)
ans = (v[-1] * p) % p

candidate = []
for i in range(16):
	residue = ((y[i]**2 - (m[i]**3 + ans * m[i])) % p)
	modified_a = (residue // m[i] + ans) ^^ e[i]
	candidate += [modified_a]

a = max(candidate, key=candidate.count)
print(candidate.count(a))

candidate = []
for i in range(16):
	b = (y[i]**2 - (m[i]**3 + (a ^^ e[i]) * m[i])) % p ^^ e[i]
	candidate += [b]

b = max(candidate, key=candidate.count)
print(candidate.count(b))
print(a)
print(b)
print(fy)
print(p)

P.<x> = PolynomialRing(Zmod(p))
f = fy^2 - x^3 - a * x - b
print(f.roots())

