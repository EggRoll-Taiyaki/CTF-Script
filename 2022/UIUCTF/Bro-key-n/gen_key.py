from output import *
from result import *

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

q = n // p

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
key = RSA.construct([n, e, d])

with open("key.pem", "wb") as f:
	f.write(key.export_key('PEM'))
