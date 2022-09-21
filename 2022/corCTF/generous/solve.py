from pwn import *
from Crypto.Util.number import long_to_bytes

def conn():

	r = remote("be.ax", 31244)
	return r

def get_param(r):

	r.recvuntil("n = ")
	n = int(r.recvline().decode().strip())
	r.recvuntil("g = ")
	g = int(r.recvline().decode().strip())
	r.recvuntil("h = ")
	h = int(r.recvline().decode().strip())

	r.recvuntil("Encrypted Flag: ")
	enc = int(r.recvline().decode().strip())

	return (n, g, h), enc

def exploit(r, pub, enc):

	n, g, h = pub
	
	r.recvuntil("Enter ciphertext> ")
	r.sendline(str(enc))
	r.recvuntil("Oracle result: ")
	lsb = int(r.recvline().decode().strip())
	
	bdd = 1 << 512
	lb, ub = 1 << 511, bdd	
	while lb + 2 < ub:
		r.recvuntil("Enter ciphertext> ")
		mid = (lb + ub) // 2
		payload = (enc * pow(g, mid, n)) % n
		r.sendline(str(payload))
		r.recvuntil("Oracle result: ")
		_lsb = int(r.recvline().decode().strip())
		if _lsb != lsb:
			ub = mid
		else:
			lb = mid

	res = ub

	lb, ub = res, bdd + res
	while lb + 2 < ub:
		r.recvuntil("Enter ciphertext> ")
		mid = (lb + ub) // 2
		payload = (enc * pow(g, mid, n)) % n
		r.sendline(str(payload))
		r.recvuntil("Oracle result: ")
		_lsb = int(r.recvline().decode().strip())
		if _lsb != lsb:
			lb = mid
		else:
			ub = mid

	p = ub - res

	print(f"p = {p}")
	print(f"flag % p = {p-res}")
	print(f"FLAG = {long_to_bytes(p-res)}")

	return 


r = conn()
pub, enc = get_param(r)
exploit(r, pub, enc)

