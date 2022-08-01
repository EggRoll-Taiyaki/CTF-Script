from pwn import *
from signature import *

r = remote("mom-can-we-have-aes.chal.uiuc.tf", 1338)

### Exchange Info
r.sendline(sig)
r.sendline("AES.MODE_ECB")
r.sendline("EASY")
for _ in range(6):
	_ = r.recvline()
	print(_)
r.sendline("finish")

### ECB Padding Oracle
flag = b"uiuctf{AES_@_h0m"
for i in range(16):
	for guess in range(256):
		prefix = ((b"\x00" * (60 - len(flag)) + flag)[-15:] + bytes([guess]) + b"\x00" * ((15 - len(flag)) % 16)).hex()
		r.sendline(prefix)
		enc = bytes.fromhex(r.recvline().decode().strip())

		if enc[:16] == enc[32:48]:
			flag += bytes([guess])
			print(flag)
			break
