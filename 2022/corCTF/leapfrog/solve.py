from output import *

"""
	g(s) = f^{n}(s) = As + B (mod p) Important A = a^n (mod p)

	Given s, g(s), g(g(s))

	g(g(s)) - g(s) = A (g(s) - s) (mod p)

	Given s, g(s), t, g(t)

	i.e. s, As + B, t, At + B
"""

s0 = out[6] - out[4]
s1 = out[10] - out[6]

t0 = out[7] - out[5]
t1 = out[9] - out[7]

"""
        s1 = s0 * a^30 (mod p)
        t1 = t0 * a^16 (mod p)
"""

_ = (s1**8 * t0**15 - s0**8 * t1**15)

"""
	M = Matrix(ZZ, 3, 3)
	M[0, 0] = out[5]
	M[0, 1] = out[7]
	M[0, 2] = 1
	M[1, 0] = out[7]
	M[1, 1] = out[9]
	M[1, 2] = 1
	M[2, 0] = out[11]
	M[2, 1] = out[12]
	M[2, 2] = 1
	print(M.determinant())
"""

kp = 210650851929872502499051168815979551475865373769294108757830840620668805680830983837146055401466217944290770121674372514801185595116308089932225711880392

from Crypto.Util.number import GCD, long_to_bytes
print(GCD(_, kp))

# FactorDB is enough :)
p = 82854189798454303629690440183768928075006051188051668052925581650741089039941

"""
	A = a^16, B = (a^16 - 1)b // (a-1)  
"""

A = ((out[9] - out[7]) * pow(out[7] - out[5], -1, p)) % p
print(A)
B = (out[7] - A * out[5]) % p
print(B)

a_list = [30764149765413907483721318469777255839684931556658737988770490182343405773892, 4109491025011411504569635067938768238229479659047949629807707819936171628565, 52090040033040396145969121713991672235321119631392930064155091468397683266049, 78744698773442892125120805115830159836776571529003718423117873830804917411376]

from Crypto.Cipher import AES
from hashlib import sha256

tmp = "05ac5b17c67bcfbf5c43fa9d319cfc4c62ee1ce1ab2130846f776e783e5797ac1c02a34045e4130f3b8111e57397df344bd0e14f3df4f1a822c43c7a89fd4113f9a7702b0b0e0b0473a2cbac25e1dd9c"
iv, ct = bytes.fromhex(tmp[:32]), bytes.fromhex(tmp[32:]) 

for a in a_list:
	assert pow(a, 16, p) == A
	b = (B * (a-1) * pow(A-1, -1, p)) % p
	key = sha256(b"".join([long_to_bytes(x) for x in [a, b, p]])).digest()[:16]
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)
	pt = cipher.decrypt(ct)
	print(pt)
