# python ecc.py > out.py

from random import randint
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha1

from typing import Tuple


class Ellipse:

    """Represents the curve x^2 + ay^2 = 1 mod p"""

    def __init__(self, a: int, p: int):

        self.a = a
        self.p = p

    def __repr__(self) -> str:
        return f"x^2 + {self.a}y^2 = 1 mod {self.p}"

    def __eq__(self, other: 'Ellipse') -> bool:
        return self.a == other.a and self.p == other.p

    def is_on_curve(self, pt: 'Point') -> bool:

        x, y = pt.x, pt.y
        a, p = self.a, self.p
        return (x*x + a * y*y) % p == 1


class Point:

    """Represents a point on curve"""

    def __init__(self, curve: Ellipse, x: int, y: int):

        self.x = x
        self.y = y
        self.curve = curve
        assert self.curve.is_on_curve(self)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: 'Point') -> 'Point':

        x, y = self.x, self.y
        w, z = other.x, other.y
        a, p = self.curve.a, self.curve.p

        nx = (x*w - a*y*z) % p
        ny = (x*z + y*w) % p
        return Point(self.curve, nx, ny)

    def __mul__(self, n: int) -> 'Point':

        assert n > 0

        Q = Point(self.curve, 1, 0)
        while n > 0:
            if n & 1 == 1:
                Q += self
            self += self
            n = n//2
        return Q

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y


def gen_secret(G: Point) -> Tuple[Point, int]:

    priv = randint(1, p)
    pub = G*priv
    return pub, priv


def encrypt(shared: Point, pt: bytes) -> bytes:

    key = sha1(str(shared).encode()).digest()[:16]
    iv = urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, 16))
    return iv + ct


def decrypt(shared: Point, ct: bytes) -> bytes:

    iv, ct = ct[:16], ct[16:]
    key = sha1(str(shared).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    return unpad(pt, 16)


a, p = 376014, (1 << 521) - 1
curve = Ellipse(a, p)

gx = 0x1bcfc82fca1e29598bd932fc4b8c573265e055795ba7d68ca3985a78bb57237b9ca042ab545a66b352655a10b4f60785ba308b060d9b7df2a651ca94eeb63b86fdb
gy = 0xca00d73e3d1570e6c63b506520c4fcc0151130a7f655b0d15ae3227423f304e1f7ffa73198f306d67a24c142b23f72adac5f166da5df68b669bbfda9fb4ef15f8e
G = Point(curve, gx, gy)

"""
sx = 1503440209141683729819659137717913014297653772909868267420574124161761461494626767959938911699905751483058221747975589371657100507759776906120012781012689244
sy = 2933381890202806090102847996698163623908379799352681467235494436992915497675358008063204354264705824168994143857597911128866633802661239882177988138033897621
shared = Point(curve, sx, sy)

ct = b'q\xfa\xf2\xe5\xe3\xba.H\xa5\x07az\xc0;\xc4%\xdf\xfe\xa0MI>o8\x96M\xb0\xfe]\xb2\xfdi\x8e\x9e\xea\x9f\xca\x98\xf9\x95\xe6&\x1fB\xd5\x0b\xf2\xeb\xac\x18\x82\xdcu\xd5\xd5\x8e<\xb3\xe4\x85e\xddX\xca0;\xe2G\xef7\\uM\x8d0A\xde+\x9fu'
flag = decrypt(shared, ct)
print(flag)
"""

if __name__ == "__main__":

    from flag import flag

    alice_pub, alice_priv = gen_secret(G)
    blake_pub, blake_priv = gen_secret(G)

    shared = alice_pub * blake_priv
    ct = encrypt(shared, flag)

    assert shared == blake_pub * alice_priv
    assert decrypt(shared, ct) == flag

    print("alice_pub =", alice_pub)
    print("blake_pub =", blake_pub)
    print("ct =", ct)
