from Crypto.Util.number import *
from Crypto.Cipher import AES
import random
import os

def USR(x, shift):
	res = x
	for i in range(32):
		res = x ^ res >> shift
	return res

def USL(x, shift, mask):
	res = x
	for i in range(32):
		res = x ^ (res << shift & mask)
	return res

def to_MT(v):
	v = USR(v, 18)
	v = USL(v, 15, 0xefc60000)
	v = USL(v, 7, 0x9d2c5680)
	v = USR(v, 11)
	return v

def to_random(y):
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & (0x9d2c5680))
    y = y ^ ((y << 15) & (0xefc60000))
    y = y ^ (y >> 18)
    return y

def xor(a, b):
	return b''.join([bytes([a[i] ^ b[i % len(b)]]) for i in range(len(a))])

def recover(a, b, c, otp):
	a = bytes_to_long(xor(a, otp))
	b = bytes_to_long(xor(b, otp))
	c = bytes_to_long(xor(c, otp))
	res = []
	MT_i, MT_iadd1, MT_iadd397 = to_MT(a), to_MT(b), to_MT(c)
	y = (MT_i & 0x80000000) + (MT_iadd1 & 0x7fffffff)
	MT_iadd624 = MT_iadd397 ^ (y >> 1)
	if (y % 2) != 0:
		MT_iadd624 = MT_iadd624 ^ 0x9908b0df
	return long_to_bytes(to_random(MT_iadd624))

def pad(s, L):

	return (L - len(s)) * b"\x00" + s

DEBUG = False

if not DEBUG:

	folder = "./enc_files/"
	files = os.listdir(folder)
	sorted_files = []
	for i in range(32):
		for fname in files:
			if fname.startswith(str(i) + "_"):
				sorted_files += [fname]
				files.remove(fname)
				break 

	enc, outputs = [], []
	for fname in sorted_files:
		with open(folder + fname, "rb") as f:
			tmp = f.read()
			enc += [tmp[:-72]]
			_ = tmp[-72:]
		for i in range(17, -1, -1):
			outputs += [_[4 * i: 4 * i + 4]]
else:
	# random.seed(12345678)
	outputs = []
	for _ in range(576):
		outputs += [long_to_bytes(random.getrandbits(32))]
	_key = long_to_bytes(random.getrandbits(1680))[:16]
	_iv = long_to_bytes(random.getrandbits(1680))[:16]

"""
	0, 1, ..., 575 (576)
	576, 577, ..., 627, 628 (1680 / 32 = 52.5)
	629, 630, ..., 680, 681
"""

for n in range(1 if DEBUG else 256**2):
	otp = pad(long_to_bytes(n), 2)

	key = recover(outputs[4], outputs[5], outputs[401], otp)[:2] + \
		pad(recover(outputs[3], outputs[4], outputs[400], otp), 4) + \
		pad(recover(outputs[2], outputs[3], outputs[399], otp), 4) + \
		pad(recover(outputs[1], outputs[2], outputs[398], otp), 4) + \
		pad(recover(outputs[0], outputs[1], outputs[397], otp), 4)[:2]
	
	iv = recover(outputs[57], outputs[58], outputs[454], otp)[:2] + \
		pad(recover(outputs[56], outputs[57], outputs[453], otp), 4) + \
		pad(recover(outputs[55], outputs[56], outputs[452], otp), 4) + \
		pad(recover(outputs[54], outputs[55], outputs[451], otp), 4) + \
		pad(recover(outputs[53], outputs[54], outputs[450], otp), 4)[:2]

	if not DEBUG:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		for i, e in enumerate(enc):
			try:
				pt = cipher.decrypt(enc[i])
				print(pt.decode())
			except:
				pass
	else:
		assert key == _key and iv == _iv
