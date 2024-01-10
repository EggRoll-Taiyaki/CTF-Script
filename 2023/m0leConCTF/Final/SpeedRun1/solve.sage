from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

K = GF(4294967311)
n = 80
m = 100

pkA, pkB, ct = load("output.sobj")

shA = []
for pka, pkb in zip(pkA, pkB):
	A, B = pka[:, :n], pka.rref()[:n, :]
	print(A*B == pka)
	shA.append((A.transpose() * pkb * B.transpose()).det())

shared = b"".join(long_to_bytes(int(x)) for x in shA)
aes = AES.new(shared, AES.MODE_ECB)
flag = aes.decrypt(bytes.fromhex(ct)) 
print(flag)
