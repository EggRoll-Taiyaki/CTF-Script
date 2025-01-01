from pwn import *
from itertools import product
from Crypto.Util.number import long_to_bytes

precision = 1000
degree = 68

R = RealField(prec=precision)
C = ComplexField(prec=precision)

scale = 2^precision
lift_Z = lambda x: ZZ(int(scale * x))

for test in range(degree * 2):

	if test % 1 == 0:
		print(test)

	server = remote("34.42.147.172", 8001)
	_ = server.recvline().decode().strip().split(" + ")
	base = C(_[0]) + C(_[1].split("*")[0]) * I

	"""
		base = e^(theta * I)
		By finite difference, we have approx of base^(a * n!) 
	"""

	def evaluate(x: int):

		server.recvuntil(b"Input")
		server.sendlineafter(b": ", str(x).encode())
		_ = server.recvline().decode().strip()
		if "+" in _:
			_ = _.split(" + ")
			return C(_[0]) + C(_[1].split("*")[0]) * I
		else:
			_ = _.split(" - ")
			return C(_[0]) - C(_[1].split("*")[0]) * I

	L = [evaluate(i) for i in range(1, degree + 2)]
	server.close()
	for i in range(degree):
		new_L = [L[i+1] / L[i] for i in range(len(L) - 1)]
		L = new_L

	m = prod([i for i in range(1, degree + 1)])
	base = base ** m

	theta1 = arccos(base.real())
	theta2 = arcsin(base.imag())
	alpha1 = arccos(L[0].real())
	alpha2 = arcsin(L[0].imag())

	for gamma1, gamma2 in product([alpha1, -alpha1], [alpha2, pi.n(precision) - alpha2, pi.n(precision) + alpha2]):
		
		theta1_p = lift_Z(theta1)
		theta2_p = lift_Z(theta2)
		gamma1_p = lift_Z(gamma1)
		gamma2_p = lift_Z(gamma2)
		m_p 	 = lift_Z((2 * pi).n(precision))

		M = Matrix(ZZ, [
			[ theta1_p,  theta2_p, 2^321,     0],
			[      m_p,         0,     0,     0],
			[        0,       m_p,     0,     0],
			[-gamma1_p, -gamma2_p,     0, 2^574]
		])
		M = M.LLL()
		for row in M:
			if row[-1] != 0:
				n = abs(row[-2] // 2^321 // (row[-1] // 2^574))
				FLAG = long_to_bytes(int(n))
				try:
					print(FLAG.decode())
				except:
					pass
