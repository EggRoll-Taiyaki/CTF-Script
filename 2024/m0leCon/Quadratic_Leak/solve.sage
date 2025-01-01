from output import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

P.<x> = PolynomialRing(ZZ)

i = 0
found = False
while not found:
	_leak = leak + i * n

	for p, _ in (x^4 - x^3 - _leak * x^2 - n * x + n^2).roots():
		if n % p == 0:
			q = n // p
			flag = long_to_bytes(pow(bytes_to_long(ciph), inverse_mod(e, (p-1)*(q-1)), n))
			print(flag)
			found = True
			break
	i += 1
