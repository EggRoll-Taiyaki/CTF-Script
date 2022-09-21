from pwn import *
import string
from itertools import product
from hashlib import sha256

alphabet = string.digits + string.ascii_letters

def conn():

	r = remote("1.13.154.182", 34727)
	return r

def proof_of_work(r):

	r.recvuntil("sha256(XXXX+")
	_ = r.recvline().decode().strip().split(") == ")
	for (X1, X2, X3, X4) in product(alphabet, repeat = 4):
		s = X1 + X2 + X3 + X4 + _[0]
		if sha256(s.encode()).hexdigest() == _[1]:
			r.sendline(s[:4])
			return

def int_to_chests(n):

	ans = ""

	for i in range(6):
		if i > 0:
			ans += " "
		if n & (1 << i):
			ans += "1"
		else:
			ans += "0"

	return ans

def int_to_question(n):

	question = ""

	for i in range(6):
		if i > 0:
			question += " and "
		if n & (1 << i):
			question += f"( B{i} == 1 )"
		else:
			question += f"( B{i} == 0 )"
	
	question = "( " + question + " )" 	

	return question

def subset_to_question(A):

	question = ""

	for i, a in enumerate(A):
		if i > 0:
			question += " or "
		question += int_to_question(a)

	return question

def query(r, question):

	r.recvuntil("Question:")
	r.sendline(question)
	r.recvuntil("Answer:")
	if b"True" in r.recvline():
		return True
	else:
		return False

def guess(r, limit = 13):

	B = []

	for i in range(6):
		if query(r, f"B{i} == 1"):
			B += [1]
		else:
			B += [0]
	
	B = B[::-1]

	state = [[], [], []]

	k = int("".join(str(b) for b in B), 2)

	state[0] += [k]

	for i in range(6):
		state[1] += [k ^ (1 << i)]

	for i in range(6):
		for j in range(i+1, 6):
			state[2] += [k ^ (1 << i) ^ (1 << j)]

	q = subset_to_question(state[1][1:]) # 7th
	cnt = 7

	if query(r, q):
		state = [[], state[0] + state[1][1:], state[1][:1]] # (0, 6, 1)

		while len(state[0]) + len(state[1]) + len(state[2]) > 1:
			if len(state[1]):
				L = len(state[1])
				q = subset_to_question(state[1][:L-(L//2)])
				if query(r, q):
					state = [[], state[1][:L-(L//2)], state[1][L-(L//2):]]
				else:
					state = [[], state[1][L-(L//2):], state[1][:L-(L//2)] + state[2]]
			else:
				L = len(state[2])
				q = subset_to_question(state[2][:L-(L//2)])
				if query(r, q):
					state = [[], [], state[2][:L-(L//2)]]
				else:
					state = [[], [], state[2][L-(L//2):]]
			cnt += 1
	else:
		print("Not finished yet")
		state = [state[0], state[1][:1], state[1][1:] + state[2]] # (1, 1, 20)

		q = subset_to_question(state[0] + state[2][:10])
		if query(r, q):
			state = [state[0], [], state[1] + state[2][:10]]
		else:
			state = [[], state[0] + state[1], state[2][10:]]
		cnt += 1

		while len(state[0]) + len(state[1]) + len(state[2]) > 1 and cnt < 14:
			if len(state[0]):
				L = len(state[2])
				q = subset_to_question(state[0] + state[2][:(L//2)-1])
				if query(r, q):
					state = [state[0], [], state[2][:(L//2)-1]]
				else:
					state = [[], state[0], state[2][(L//2)-1:]]
			elif len(state[1]) > 1:
				L = len(state[2])
				q = subset_to_question(state[1][:1] + state[2][:L-(L//2)])
				if query(r, q):
					state = [[], state[1][:1], state[1][1:] + state[2][:L-(L//2)]]
				else:
					state = [[], state[1][1:], state[1][:1] + state[2][L-(L//2):]]
			else:
				L = len(state[2])
				q = subset_to_question(state[2][:L-(L//2)])
				if query(r, q):
					state = [[], [], state[1] + state[2][:L-(L//2)]]
				else:
					state = [[], state[1], state[2][L-(L//2):]]
			cnt += 1
	
	for _ in range(cnt, limit):
		query(r, "1 == 1")

	print(state)
	n = (state[0] + state[1] + state[2])[0]

	r.recvuntil("Now open the chests:")
	ans = int_to_chests(n)
	r.sendline(ans)

	r.recvline()
	_ = r.recvline()
	print(_)

	return

r = conn()
proof_of_work(r)
for _ in range(50):
	print(f"Round {_}")
	guess(r, 13)
r.interactive()
