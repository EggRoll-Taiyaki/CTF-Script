from Crypto.Util.number import *
from output import *

"""
	slope = (3 * x**2 + a) / (2 * y)
	x = slope**2 - 2 * x
	3 * x = slope**2
	3 * x * (2 * y)^2 = (3 * x**2 + a)^2 (mod p)
	-y = slope * (x - (slope**2 - 2 * x)) - y (mod p)

	x^3 + a * x + b = y^2 (mod p)
"""

"""
	Sage code for solving a

	for i in range(32):
		P.<a> = PolynomialRing(Zmod(n))
		poly = (3 * gx**2 + (i << 120) + a)^2 - (3 * gx * (2 * gy)^2)
		B = 0.35
		_ = poly.small_roots(X = 2^120, beta = B, epsilon = B**2 - 120 / 1023)
		print(i)
		print(_)	
"""

a = (24 << 120) + 1141587253239793338029408616598837591

p = GCD(n, (3 * gx**2 + a)**2 - (3 * gx * (2 * gy)**2))
q = n // p

b = (gy**2 - gx**3 - a * gx) % p
c = pow(ct, pow(0x10001, -1, (p-1)*(q-1)), n)
c >>= (512 - 125)

FLAG = long_to_bytes((a << 250) + (b << 125) + c)
print(FLAG)

