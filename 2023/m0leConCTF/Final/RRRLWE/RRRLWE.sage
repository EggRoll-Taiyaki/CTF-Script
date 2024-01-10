from Crypto.Util.number import bytes_to_long
from random import randint
from secret import flag

n = 2^10
qc = 2^22
qm = 2^8
P = PolynomialRing(Integers(qc), 'x')
x = P.gen()
Pq = P.quotient(x^n-1, 'y')
y = Pq.gen()

def gen_data(m,s):
	a = Pq.random_element()
	mask = Pq.random_element()*(y-1)
	e = sum([y^i * (randint(0,2^4)-2^3) for i in range(n)])
	b = s*a + m + mask + qm*e
	return [b,a]

pad = hex(bytes_to_long(flag))[2:]
newpad = [pad[i:i+12] for i in range(0, len(pad), 12)]
data = []

for i in newpad:
	s = Pq.random_element()
	for j in [i[k:k+2] for k in range(0, len(i), 2)]:
		data.append(gen_data(int(j,16), s))

print(f"{data = }")
