from pubkey import pub

"""
	p: 114 bits
	q: 514 bits
	r: 191 bits

	x0 = p0 * q + 2 * r
	xi = pi * q + 2 * r 

	xi: 114 + 514 = 628 bits

	di = p0 * xi - pi * x0 = 2 * (p0 - pi) * r

	di: 1 + 114 + 191 = 306 bits
"""

def recover_pi(i, n): 
	
	M = Matrix(ZZ, n+1, n+1)

	M[0, 0] = 2^(1 + 191)
	for j in range(n):
		M[0, j+1] = pub[(i+j+1) % len(pub)]
		M[j+1, j+1] = -pub[i]

	L = M.LLL()
	pi = abs(L[0, 0] // M[0, 0])

	if pi.is_prime():
		return pi
	else:
		return None

p = []

for i in range(len(pub)):
	p += [recover_pi(i, 40)]

lb, ub = 2^513, 2^514

for i in range(len(p)):
	# sk = (x - 2 * ri) // pi 
	# (x - 2 * ub) // pi < sk < (x - 2 * lb) // pi
	lb = max(lb, (pub[i] - 2^192) // p[i])
	ub = min(ub, (pub[i] - 2^191) // p[i])

print(lb + ub) # approx_sk

