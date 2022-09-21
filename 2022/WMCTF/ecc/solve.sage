from Crypto.Util.number import *
from output import *

"""
	y1^2 = x1^3 + ax1 + b (mod n)
	y2^2 = x2^3 + ax2 + b (mod n)
"""

a = pow(px - gx, -1, n) * ((py**2 - px**3) - (gy**2 - gx**3)) % n
b = (gy**2 - gx**3 - a * gx) % n

E = EllipticCurve(Zmod(n), [a, b])
G = E(gx, gy)
P = 3 * G
p = GCD(px - int(P.xy()[0]), n)
q = n // p

pt = pow(c, pow(e, -1, (p-1)*(q-1)), n)
a = (pow(px - gx, -1, p) * ((py**2 - px**3) - (gy**2 - gx**3))) % p
b = (gy**2 - gx**3 - a * gx) % p

E = EllipticCurve(Zmod(p), [a, b])
G = E(gx, gy)
assert 3 * G == E(px, py)

print(a)
print(b)
print(pt)

