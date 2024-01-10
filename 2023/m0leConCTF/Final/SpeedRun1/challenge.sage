from secret import flag
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

K = GF(4294967311)
n = 80
m = 100


def keygen():
    sk = []
    pk = []
    for _ in range(4):
        A = random_matrix(K, m, n)
        B = random_matrix(K, n, m)
        sk.append((A, B))
        pk.append(A*B)
    return (sk, pk)


def dh(sk, pk):
    shared = []
    for csk, cpk in zip(sk, pk):
        A, B = csk
        shared.append((A.transpose() * cpk * B.transpose()).det())
    return shared



skA, pkA = keygen()
skB, pkB = keygen()

shA = dh(skA, pkB)
shB = dh(skB, pkA)

assert shA == shB


shared = b"".join(long_to_bytes(int(x)) for x in shA)
aes = AES.new(shared, AES.MODE_ECB)
ct = aes.encrypt(flag.encode())


save((pkA, pkB, ct.hex()), "output")
