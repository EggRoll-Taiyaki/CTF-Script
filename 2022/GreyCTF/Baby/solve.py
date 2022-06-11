from output import *

def egcd(b: int, n: int):

	(x0, x1, y0, y1) = (1, 0, 0, 1)
	while n != 0:
		(q, b, n) = (b // n, n, b % n)
		(x0, x1) = (x1, x0 - q * x1)
		(y0, y1) = (y1, y0 - q * y1)
	return (b, x0, y0)

b, x0, y0 = egcd(r, s)

x0 *= hint // b
y0 *= hint // b

assert x0 * r + y0 * s == hint

p = x0 % s 
assert p.bit_length() == 1024

q = -y0 % r
assert q.bit_length() == 1024

m = pow(c, pow(0x10001, -1, (p-1) * (q-1)), p * q)

from Crypto.Util.number import long_to_bytes

flag = long_to_bytes(m)
print(flag)

