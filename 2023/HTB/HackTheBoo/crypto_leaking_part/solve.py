from out import *
from Crypto.Util.number import *
import math
from sympy import nextprime
import itertools 

MAX = 0x100

factors = []
numb = leak
for i in range(int(math.log2(MAX))):
	for j in range(MAX, -1, -1):
		if isPrime(j) and numb % j == 0:
			P = nextprime(j)
			numb //= math.prod(range(1, P))
			factors += [P]
			break

assert len(factors) == 8 and numb == 1

for fs in itertools.combinations(factors, 4):
	p = 1
	for i in fs:
		p *= math.prod(range(1, i))
	p = nextprime(p)
	q = nextprime(leak // p)
	print("+1")
	try:
		m = pow(c, pow(e, -1, (p-1)*(q-1)), p*q) 
		flag = long_to_bytes(m)
		if b"HTB" in flag:
			print(flag)
	except:
		pass

