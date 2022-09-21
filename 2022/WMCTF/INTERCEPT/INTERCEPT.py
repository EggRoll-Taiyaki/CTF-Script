import os
import string
import signal
from gmpy2 import *
from Crypto.Util.number import *
from hashlib import sha256, sha512, md5
from random import randint, seed, choice

class KGC:
    def __init__(self, lam):
        
        self.lam = lam
        while 1:
            self.z = 2 * randint(1 << 63, 1 << 64)
            self.p = self.genPrime(self.z)
            self.q = self.genPrime(2)
            self.N = (self.z * self.p + 1) * (2 * self.q + 1)
            
            self.s1, self.s2 = randint(1, self.N), randint(1, self.N)
            if self.s1 % 2 == self.s2 % 2: 
                self.s1 += 1
            
            self.g = randint(1, self.N)
            check = pow(self.g, self.p * self.q, self.N) != 1 and pow(self.g, self.z * self.p, self.N) != 1 and pow(self.g, self.z * self.q, self.N) != 1
            while not check:
                self.g = randint(1, self.N)
                check = pow(self.g, self.p * self.q, self.N) != 1 and pow(self.g, self.z * self.p, self.N) != 1 and pow(self.g, self.z * self.q, self.N) != 1
            
            break
        
        self.g1, self.g2, self.g3 = (pow(self.g, self.p * self.s1, self.N),
                    pow(self.g, self.p * self.s2, self.N),
                    pow(self.g, self.p ** 2, self.N))
    
    def genPrime(self, delta):
        prime = 1
        while not isPrime(prime):
            prime = delta * getPrime(self.lam // 2 - delta.bit_length()) + 1
        return (prime - 1) // delta
    
    def H1(self, m):
        return int(sha256(m.encode()).hexdigest(), 16)
    
    def H2(self, m):
        return int(sha512(m.encode()).hexdigest(), 16)
    
    def H3(self, m):
        return int(md5(m.encode()).hexdigest(), 16)
    
    def KeyGen(self, username):
        h1, h2 = self.H1(username), self.H2(username)
        y1 = invert(self.p, self.z * self.q) * h1 % (self.z * self.q)
        y2 = invert(self.p, self.z * self.q) * h2 % (self.z * self.q)
        d = invert(y1 * self.s1 + y2 * self.s2, self.z * self.q)
        e = pow(self.g1, h1, self.N) * pow(self.g2, h2, self.N) % self.N
        
        return (y1, y2, d, h1, h2, e)
    
    def enc(self, m, user):
        length_limit = 2**128
        r = randint(1, self.N)
        F = pow(self.g3, r, self.N)
        c1 = (m % length_limit) ^ self.H3(str(F))
        c2 = pow(user.e, r, self.N)
        return (c1, c2)
    
    def dec(self, c, user):
        c1, c2 = c
        F = pow(c2, user.d, self.N)
        m = long_to_bytes(self.H3(str(F)) ^ c1)
        return m


class USER:
	def __init__(self, id_, kgc):
		self.id_ = id_
		self.y1, self.y2, self.d, self.h1, self.h2, self.e = kgc.KeyGen(id_)
    
	def print_info(self):
		print(f'e, d, h1, h2 = ({self.e}, {self.d}, {self.h1}, {self.h2})')

def register(username, kgc):
    user = USER(username, kgc)
    return user
        
def intercept():
    while True:
        try:
            informant = 'WMCTF_IS_FUN_' + str(getRandomNBitInteger(512)) # randomize a big string
            USERLIST[informant] = register(informant, kgc)
            INFORMATION = randint(1 << 127, 1 << 128)
            return informant, INFORMATION
        except:
            pass

def determinant(row1, row2, row3):

	return (row1[0] * (row2[1] * row3[2] - row2[2] * row3[1]) \
		- row1[1] * (row2[0] * row3[2] - row2[2] * row3[0]) \
		+ row1[2] * (row2[0] * row3[1] - row2[1] * row3[0]))

if __name__ == "__main__":
    
	LAM = 512
	LIMITED_USER_NUM = 5
	kgc = KGC(LAM)
	zq = kgc.z * kgc.q
	USERLIST = {}
	informant, INFORMATION = intercept()

	users = [chr(ord("A") + i) for i in range(26)]

	print(f'Here gives you some params about the KGC: {kgc.N}, ({kgc.g1}, {kgc.g2}, {kgc.g3})')
         
	"""
		y1 = invert(self.p, self.z * self.q) * h1 % (self.z * self.q)
		y2 = invert(self.p, self.z * self.q) * h2 % (self.z * self.q)
		d = invert(y1 * self.s1 + y2 * self.s2, self.z * self.q)
		e = pow(self.g1, h1, self.N) * pow(self.g2, h2, self.N) % self.N
	
		d * (y1 * s1 + y2 * s2) = 1 (mod zq)
		d * (h1 * (s1 / p) + h2 * (s2 / p)) = 1 (mod zq)
		(d * h1) * (s1 / p) + (d * h2) * (s2 / p) = 1 (mod zq)
	"""

	rows = []

	for username in users:
		try:
			if username not in USERLIST:
				USERLIST[username] = register(username, kgc)
				print('Registration success, keep your account well!')
				y1 = USERLIST[username].y1
				y2 = USERLIST[username].y2
				d = USERLIST[username].d
				h1 = USERLIST[username].h1
				h2 = USERLIST[username].h2
				e = USERLIST[username].e
				rows += [[d * h1, d * h2, 1]]
			else:
				print('This username has been taken!')
		except:
			print('Registration Not Allowed!')

		if len(rows) >= LIMITED_USER_NUM:
			break

	print(len(rows))
	L = len(rows)

	_zq = determinant(rows[0], rows[1], rows[2])

	for i in range(L):
		for j in range(i+1, L):
			for k in range(j+1, L):
				_zq = GCD(_zq, determinant(rows[i], rows[j], rows[k]))

	assert _zq == zq

	print(zq.bit_length())

	"""
		a1 x + b1 y = 1 (mod m)
		a2 x + b2 y = 1 (mod m)

		(b2 * a1 - b1 * a2) x = b2 - b1 (mod m)
	"""
	
	s1p = pow(rows[1][1] * rows[0][0] - rows[0][1] * rows[1][0], -1, _zq) * (rows[1][1] - rows[0][1]) % _zq
	assert s1p == (kgc.s1 * pow(kgc.p, -1, _zq)) % _zq
	s2p = (1 - rows[0][0] * s1p) * pow(rows[0][1], -1, _zq) % _zq

	print(informant)

	d = pow(kgc.H1(informant) * s1p + kgc.H2(informant) * s2p, -1, _zq)

	assert d == USERLIST[informant].d
