from pwn import *

def conn():

	return remote("accessible-sesasum-indicum.chal.irisc.tf", 10104)

def luck_test(server, s):
		
	server.sendlineafter(b"Attempt> ", s)

with open("output.txt", "r") as f:
	f.readline()
	s = f.readline()

server = conn()
for _ in range(16):
	luck_test(server, s)
server.interactive()
