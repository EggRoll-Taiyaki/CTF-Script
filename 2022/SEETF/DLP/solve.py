from params import *

"""
	Assume m = m0 + m1p + m2p^2 + ...

	g  = gp[0]  + gp[1]p  + gp[2]p^2  + ... + gp[w-1]p^(w-1)
	gm = gmp[0] + gmp[1]p + gmp[2]p^2 + ... + gmp[w-1]p^(w-1)

	We can find m0 and now,

	gm  = g^m0 * (g^p)^(m1 + m2p^2 + ...)
	gm' = (g^p)^(m1 + m2p^2 + ...)

	lift g to g^p and find mk recursively
"""


primes, power = n
res, mod = [], []
prod = 1
for p, w in zip(primes, power):
	
	prod *= (p ** w)

	if w == 1:
		res += [0]
	elif w == 2:
		a = (g % (p ** 2) - 1) // p
		b = (gm % (p ** 2) - 1) // p
		m = pow(a, -1, p) * b % p
		assert pow(g, m, p ** w) == gm % (p ** w)
		res += [m]
	else:
		a = w // 2
		c1 = pow(gm, p ** (w - 1 - a), p ** w)
		y1 = pow(g , p ** (w - 1 - a), p ** w)
		m1 = pow((y1 - 1) // (p ** (w - a)), -1, p ** a) * ((c1 - 1) // (p ** (w - a))) % (p ** a)
		c2 = gm * pow(g, -m1, p ** w)
		y2 = pow(g, p ** a, p ** w)
		m2 = pow((y2 - 1) // (p ** (a + 1)), -1, p ** (w - 1 - a)) * ((c2 - 1) // (p ** (a + 1))) % (p ** (w - 1 - a))
		m = m1 + m2 * (p ** a)
		assert pow(g, m, p ** w) == gm % (p ** w)
		res += [m]
	
	mod += [p ** (w - 1)]

from hashlib import sha256

print("SEE{%s}" % sha256(mm.to_bytes((mm.bit_length()+7)//8, "little")).hexdigest())

# assert pow(g, mm, prod) == gm
# print(f"res = {res}")
# print(f"mod = {mod}")
