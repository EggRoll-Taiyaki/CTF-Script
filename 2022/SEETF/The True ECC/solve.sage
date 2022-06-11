from true_ecc_output import *

a, p = 376014, (1 << 521) - 1

F.<v> = PolynomialRing(GF(p))
f = v^2 + a
K = F.quo(f)
w = K.gen()

gx = 0x1bcfc82fca1e29598bd932fc4b8c573265e055795ba7d68ca3985a78bb57237b9ca042ab545a66b352655a10b4f60785ba308b060d9b7df2a651ca94eeb63b86fdb
gy = 0xca00d73e3d1570e6c63b506520c4fcc0151130a7f655b0d15ae3227423f304e1f7ffa73198f306d67a24c142b23f72adac5f166da5df68b669bbfda9fb4ef15f8e

G = GF(p)(gx) + GF(p)(gy) * w
A = GF(p)(ax) + GF(p)(ay) * w
B = GF(p)(bx) + GF(p)(by) * w

dA = discrete_log(A, G, 2^520, operation = "*")
shared = B^dA
print(shared)
