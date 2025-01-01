from output import *
import hashlib
from Crypto.Util.number import *

m = ['Hi', 'How are you doing?', 'here are some signatures',
	'for you to understand how this works', 'have fun']

def hash(msg):
	return Integer('0x' + hashlib.sha256(msg.encode()).hexdigest())

"""
	s1 = (K + k1 * q)^(-1) * (m1 + d * r1)
	s2 = (K + k2 * q)^(-1) * (m2 + d * r2)
	
	K + k1 * q = m1 / s1 + d * (r1 / s1)
	K + k2 * q = m2 / s2 + d * (r2 / s2)

	(k1 - k2) * q = (m1 / s1 - m2 / s2) + d * (r1 / s1 - r2 / s2)
	k1 - k2 = (m1 / (q * s1) - m2 / (q * s2)) + d * (r1 / (q * s1) - r2 / (q * s2)) 
"""

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
q = floor(1.337*sqrt(n))

e = [hash(mi) for mi in m]

a, b = [], []
for i in range(len(m)):
	for j in range(i+1, len(m)):
		a += [r[j] * inverse_mod(q * s[j], n) - r[i] * inverse_mod(q * s[i], n)]
		b += [e[j] * inverse_mod(q * s[j], n) - e[i] * inverse_mod(q * s[i], n)]
M = Matrix(ZZ, len(a) + 2, len(a) + 2)
for i in range(len(a)):
	M[  0, i] = q * a[i]
	M[ -1, i] = q * b[i]
	M[1+i, i] = q * n
M[ 0, -2] = 1
M[-1, -1] = q
"""
	[a[0], a[1], a[2], a[3], 1, 0],
	[   n,    0,    0,    0, 0, 0],
	[   0,    n,    0,    0, 0, 0],
	[   0,    0,    n,    0, 0, 0],
	[   0,    0,    0,    n, 0, 0],
	[b[0], b[1], b[2], b[3], 0, q]
"""
M = M.LLL()
for row in M.rows():
	FLAG = long_to_bytes(int(abs(row[-2])))
	try:
		print(FLAG.decode())
	except:
		pass
