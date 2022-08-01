from Crypto.Util.number import *
from output import *

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
lim = 7
factors = [10357495682248249393, 10441209995968076929, 10476183267045952117, 11157595634841645959, 11865228112172030291, 12775011866496218557, 13403263815706423849, 13923226921736843531, 14497899396819662177, 14695627525823270231, 15789155524315171763, 16070004423296465647, 16303174734043925501, 16755840154173074063, 17757525673663327889, 18318015934220252801]

for i in range(1 << 16):
	if bin(i)[2:].count("1") != 8:
		continue

	_p, _q = 1, 1
	for j in range(16):
		if i & (1 << j):
			_p *= factors[j]
		else:
			_q *= factors[j]

	p, q = None, None
	for j in range(lim):
		if isPrime(_p+1):
			p = _p + 1
		_p *= small_primes[j]

	for j in range(lim):
		if isPrime(_q+1):
			q = _q + 1
		_q *= small_primes[j]

	if p and q:
		n = p * q
		m = pow(ct, d, n)
		FLAG = long_to_bytes(m)
		if b"uiu" in FLAG:
			print(FLAG)
