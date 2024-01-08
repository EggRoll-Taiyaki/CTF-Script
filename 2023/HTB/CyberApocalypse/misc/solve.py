from pwn import *

def conn():

	r = remote("68.183.45.143", 31324)
	return r

def S(r):

	r.recvuntil(b"Below are the estimates of how long each of us will take to cross the bridge and the charge left for the flashlight")
	for _ in range(2):
		r.recvline()
	v = []
	idx = 1
	while True:
		_ = r.recvline()
		if b"Person" in _:
			v += [(idx, int(_.decode().split("will take ")[1].split(" minutes to cross the bridge")[0]))]
		else:
			print(_) # debug
			break
		idx += 1
	v.sort(key = lambda x : x[1])
	strategy = ""
	ans = 0
	print(v)
	while len(v) >= 4:
		planA = 2 * v[0][1] + v[-2][1] + v[-1][1]
		planB = v[0][1] + 2 * v[1][1] + v[-1][1]
		if len(strategy):
			strategy += ","
		if planA < planB:
			strategy += f"[{v[0][0]},{v[-2][0]}],[{v[0][0]}],[{v[0][0]},{v[-1][0]}],[{v[0][0]}]"
			ans += planA
		else:
			strategy += f"[{v[0][0]},{v[1][0]}],[{v[0][0]}],[{v[-2][0]},{v[-1][0]}],[{v[1][0]}]"
			ans += planB
		
		v = v[:-2]
	if len(v) == 3:
		if len(strategy):
			strategy += ","
		strategy += f"[{v[0][0]},{v[2][0]}],[{v[0][0]}],[{v[0][0]},{v[1][0]}]"
		ans += v[0][1] + v[1][1] + v[2][1]
	elif len(v) == 2:
		if len(strategy):
			strategy += ","	
		strategy += f"[{v[0][0]},{v[1][0]}]"
		ans += v[1][1]
	else:
		strategy += f"[{v[0][0]}]"
		ans += v[0][1]
	
	print(ans)
	print(strategy)

	r.sendlineafter(b"> ", strategy.encode())
	r.interactive()

r = conn()
r.sendlineafter(b"> ", b"2")
S(r)
