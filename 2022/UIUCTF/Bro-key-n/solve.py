from output import *
from Crypto.Util.number import *

k = 512
m = 1 << k

p_lower_bits = (n % m) * pow(q_lower_bits, -1, m) % m 

for i in range(1, e):
	dp_lower_bits = (i * (p_lower_bits - 1) + 1) * pow(e, -1, m) % m
	for j in range(16):
		dp = dp_high_bits + j * m + dp_lower_bits	

		p = ((dp * e - 1) // i) + 1
		if isPrime(p):
			if n % p == 0:
				print(f"Found!")
				print(p)
				print(n // p)
				break

	if i % 1000 == 0:
		print(i)
