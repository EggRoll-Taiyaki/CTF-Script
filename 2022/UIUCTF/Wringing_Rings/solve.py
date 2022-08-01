out = [
       (1, 744415),
       (3, 462408803),
       (4, 4363587298),
       (5, 26302792823),
       (6, 117400352930),
       (7, 422820345595),
       (8, 1296720040658),
       (9, 3510114195023),
       (10, 8599471806418)
]

mod = []
res = []
M = 1
for x, fx in out:
    mod += [x]
    res += [fx % x]
    M = lcm(M, x)
r = crt(res, mod)

P.<x> = PolynomialRing(QQ)
for i in range((500_000 - r) // M + 2):
	f = P.lagrange_polynomial(out + [(0, r + i * M)])
	coef = f.list()

	check = True
	for j in range(10):
		if coef[j].is_integer() == False:
			check = False
		else:
			if coef[j] > 100_000:
				check = False

	if check:
		print(r + i * M)
    
