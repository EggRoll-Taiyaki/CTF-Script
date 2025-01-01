from out import *
import hashlib
from Crypto.Util.number import *

class testhash:
	def __init__(self, data):
		self.data = data

	def digest(self):
		return self.data 

hashes = []
hashes.append(testhash) 
hashes.append(hashlib.md5)
hashes.append(hashlib.sha224)
hashes.append(hashlib.sha256)
hashes.append(hashlib.sha3_224)
hashes.append(hashlib.sha3_256)

message1 = "SmallCatCat".encode('utf-8')
s1 = sum([bytes_to_long(hash_object(message1).digest()) * r for hash_object, r in zip(hashes, sig1)]) - sig1[-1]
message2 = "SmallDogDog".encode('utf-8')
s2 = sum([bytes_to_long(hash_object(message2).digest()) * r for hash_object, r in zip(hashes, sig2)]) - sig2[-1]

p = GCD(s1, s2)
for i in range(2, 1000):
	while p % i == 0:
		p //= i

B = [1] * 6
M = Matrix(ZZ, [
	[ sig[0], B[0],    0,    0,    0,    0,    0, 0],
	[ sig[1],    0, B[1],    0,    0,    0,    0, 0],
	[ sig[2],    0,    0, B[2],    0,    0,    0, 0],
	[ sig[3],    0,    0,    0, B[3],    0,    0, 0],
	[ sig[4],    0,    0,    0,    0, B[4],    0, 0],
	[ sig[5],    0,    0,    0,    0,    0, B[5], 0],
	[      p,    0,    0,    0,    0,    0,    0, 0],
	[-sig[6],    0,    0,    0,    0,    0,    0, 2^1000]	
])
M = M.LLL()
for row in M.rows():
	if row[0] == 0 and abs(row[-1]) == 2^1000:
		print(long_to_bytes(int(abs(row[1]))))
