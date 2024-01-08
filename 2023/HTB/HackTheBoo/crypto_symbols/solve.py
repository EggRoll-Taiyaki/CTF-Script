from out import *

p = 307163712384204009961137975465657319439
g = 1337

bits = ""
for gr in out:
	if pow(gr, (p-1)//2, p) == 1:
		bits += "0"
	else:
		bits += "1"

m = int(bits, 2)			
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
