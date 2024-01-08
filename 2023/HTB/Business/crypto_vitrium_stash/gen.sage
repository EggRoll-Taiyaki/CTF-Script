from Crypto.Util.number import *
import json

q = 26189572440233739420990528170531051459310363621928135990243626537967

# b'{"admin": True, "user": "xxxxxxx"}'

for k in range(30, 70):
	
	c = bytes_to_long(b'{"admin": true, "user": "' + b"\x00" * k + b'"}')
	M = Matrix(ZZ, k+2, k+2)
	M[:k+1, :k+1] = Matrix.identity(k+1)
	for i in range(k):
		M[i, -1] = 256 ** (k+1 - i)
		M[-2, i] = -80
	M[-2, -2] = 1
	M[-2, -1] = c
	M[-1, -1] = -q
	M = M.LLL()

	for r in M:
		if r[-1] == 0 and r[-2] == 1:
			try:
				print("Found")
				print(k)
				user = "".join([chr(r[i] + 80) for i in range(k)])
				# check
				message = b'{"admin": true, "user": "' + user.encode() + b'"}'
				print(bytes_to_long(message) % q)
				print(message.decode())
			except:
				pass
