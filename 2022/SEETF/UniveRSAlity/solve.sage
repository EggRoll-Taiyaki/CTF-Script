import json
from Crypto.Util.number import *

p = 314159265358979349999999999999999950327
q = 271828182845904549999999999999999990481

token = "tjzBcpbqoZw"

js = json.dumps({'token': token})
m = bytes_to_long(js.encode())
c = pow(m, 0x10001, p * q)

for i in range(10):
	forge_js = '{"token":"' + token + '","flag":' + str(i) + '}'
	forge_m = bytes_to_long(forge_js.encode())

	assert forge_m < p * q

	try:
		rp = discrete_log(GF(p)(forge_m), GF(p)(c), operation = "*")
		rq = discrete_log(GF(q)(forge_m), GF(q)(c), operation = "*")

		d = crt([rp, rq], [p - 1, q - 1])

		assert pow(c, d, p * q) == forge_m

		print(d)

	except:
		pass



