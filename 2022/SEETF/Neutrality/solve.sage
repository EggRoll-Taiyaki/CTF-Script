with open("neural_output.txt") as f:
	_ = f.readlines()

def toVec(n):
	v = []
	for i in range(40 * 8):
		if n & (1 << i):
			v += [1]
		else:
			v += [-1]
	return v

M = Matrix(ZZ, 320, 200 + 320)
a = 2^50

for i in range(200):
	n = int(_[i][:-1])
	v = toVec(n)
	for j in range(320):
		M[j, i] = a * v[j]
		M[j, j + 200] = 1

L = M.LLL()
L = L.BKZ(block_size = 10)
for i in range(320):
	v = list(L[i])
	if v[:200].count(0) == 200 and v[200:].count(1) + v[200:].count(-1) == 320:
		print(v[200:])
		break
