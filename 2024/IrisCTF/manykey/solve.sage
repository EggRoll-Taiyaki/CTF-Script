from pwn import remote
from ecdsa import SigningKey, VerifyingKey, util
from ecdsa.curves import Curve
from ecdsa.ellipticcurve import CurveFp, PointJacobi
from hashlib import sha1
from Crypto.Util.number import *

def conn():

	return remote("manykey.chal.irisc.tf", 10102)

def get_sig(server):

	server.recvuntil("Hello,")
	msg = bytes.fromhex(server.recvline().decode())
	sig = bytes.fromhex(server.recvline().decode())

	return (msg, sig)

def get_pub(server):
	
	server.recvuntil("Here's my public key")
	server.recvline()
	vk = VerifyingKey.from_der(bytes.fromhex(server.recvline().decode()))

	return vk

server = conn()
(msg, sig) = get_sig(server)
vk = get_pub(server)

assert vk.verify(sig, msg, sha1)

pk = vk.pubkey
r, s = util.string_to_number_fixedlen(sig[:len(sig)//2], pk.generator.order()), util.string_to_number_fixedlen(sig[len(sig)//2:], pk.generator.order())

h = bytes_to_long(sha1(msg).digest())

def smart_dlog(P, Q, p):
	E = P.curve()
	Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

	P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
	for P_Qp in P_Qps:
		if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
			break

	Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
	for Q_Qp in Q_Qps:
		if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
			break

	p_times_P = p * P_Qp
	p_times_Q = p * Q_Qp

	x_P,y_P = p_times_P.xy()
	x_Q,y_Q = p_times_Q.xy()

	phi_P = -(x_P/y_P)
	phi_Q = -(x_Q/y_Q)
	k = phi_Q/phi_P
	return ZZ(k)

### DLOG friendly curve
p = 4546783968475597180640562402424788742080260810198314176247
a = 3890987587994294890387347526685361731909761857754937020972
b = 3865461739013920837489244550027500609450523367473509037996

order = p
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
assert G.order() == order

P = E.lift_x(GF(p)(r))
k = smart_dlog(G, P, p)
assert k * G == P
d = int((k * s - h) * pow(r, -1, p) % p)

curve = CurveFp(p, a, b, 1)
generator = PointJacobi(curve, int(G.xy()[0]), int(G.xy()[1]), 1, order)
ec = Curve(
	"Smart", 
	curve, 
	generator, 
	None
)

sk2 = SigningKey.from_secret_exponent(d, ec)
vk2 = sk2.verifying_key
assert sk2.privkey.secret_multiplier * sk2.curve.generator == vk2.pubkey.point
assert vk2.verify(sig, msg)
server.sendlineafter(b"What was my private key again?", sk2.to_der().hex())
server.recvline()
print(server.recvline())
