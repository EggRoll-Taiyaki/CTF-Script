from Crypto.Util.number import bytes_to_long
from random import randint

n = 2^10
qc = 2^22
qm = 2^8
P = PolynomialRing(Integers(qc), 'x')
x = P.gen()
Pq = P.quotient(x^n-1, 'y')
y = Pq.gen()

load('output.sage')

flag = b""
for i in range(0, len(data), 6):

	### b = s*a + m + mask + qm*e
	enc = []
	for b, a in data[i: i+6]:
		### Eliminate mask 
		_a = a.lift() % (x - 1)
		_b = b.lift() % (x - 1) 
		### Drop qm*e 
		_a = _a.change_ring(Zmod(256))
		_b = _b.change_ring(Zmod(256))
		enc += [(_b, _a)]

	candidates = []
	for _s in range(256):
		tmp = [int(_b - _s*_a) for (_b, _a) in enc]

		if all([(30 <= c <= 127) for c in tmp]):
			candidates += [bytes(tmp)]
	
	print(f"The candidates for {i // 6}-th piece of flag.")
	for idx in range(len(candidates)):
		print(f"{idx}: {candidates[idx]}")
	
	idx = int(input("Choose the piece: "))
	asset 0 <= idx < len(candidates)
	flag += candidates[idx]
	print(flag)
	print()
