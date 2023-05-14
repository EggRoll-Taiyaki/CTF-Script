from output import *
import hashlib

N = 64

Q = matrix(ZZ, N, N, Q)
M1 = matrix(ZZ, N, N, M1)
M2 = matrix(ZZ, N, N, M2)

# https://en.wikipedia.org/wiki/Circulant_matrix
C = ComplexField(1024)
r = exp(2 * I * pi / N)
F = matrix(C, [[C(r^(j*k)) for k in range(N)] for j in range(N)])

"""
Diagonalize secert matrix U --> 1/F * D * F
M1 = U.T * Q * U = (1/F * D * F).T * Q * (1/F * D * F)
		 = F.T * D * 1/F.T * Q * 1/F * D * F
1/F.T * M1 * 1/F = D * (1/F.T * Q * 1/F) * D
Define f(M) = 1/F.T * M * 1/F, then f(M1) = D * f(Q) * D
"""

fQ = 1/F.T * Q / F
fM1 = 1/F.T * M1 / F

# This failed <-- [sqrt(fM1[i, i] / fQ[i, i]) for i in range(N)]
# Thanks A~Z for better computation
d = [sqrt(fM1[0, 0] / fQ[0, 0])]
for i in range(1, N):
	d += [fM1[0, i] / (d[0] * fQ[0, i])]
D = matrix.diagonal(C, d)

U = 1/F * D * F
S1 = U.T * M2 * U

# resolve floating error
S1 = matrix(ZZ, N, N, [round(s.real()) for s in S1.list()])

ss = hashlib.sha256(str(S1).encode()).digest()
flag = bytes([x^^y for x, y in zip(bytes.fromhex(enc), ss)])
print(flag)
