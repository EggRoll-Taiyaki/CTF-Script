import point
from itertools import product

p = 47

L = list(range(p))

cnt = 0

for _ in product(L, L, L, L):
	a, b, c, d = _
	if (a*a + b*b + c*c + d*d) % p == 1:
		cnt += 1

assert cnt == (p - 1) * p * (p + 1)


