from params import *
from mt19937predictor import MT19937Predictor
import random

primes, power = n
m = 1
for p, w in zip(primes, power):
	m *= (p ** w)

for p, w in zip(primes, power):
	for i in range(w-1, 0, -1):
		if pow(g, p ** i, p ** w) != 1:
			print(i + 1)
			print(w)
			print()
			break

g = random.randint(0, m - 1)

predictor = MT19937Predictor()
for _ in range(624):
	x = g % (1 << 32)
	predictor.setrandbits(x, 32)
	g >>= 32

for _ in range(10):
	x = g % (1 << 32)
	assert x == predictor.getrandbits(32)
	g >>= 32

