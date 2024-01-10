import random

MAX_DIGITS = 65536

S = list("0123456789abcdef")

appeared = []
cur = ["z" for _ in range(4)]
counter = 0
Attempt = ""
while counter < MAX_DIGITS:
	appeared += [cur]
	counter += 1
	candidate = []
	found = False
	for next in [[c] + cur[:3] for c in S]:
		if next not in appeared:
			candidate += [next[0]]
			found = True
	if not found:
		c = random.choice(S)
		Attempt += c
		cur = [c] + cur[:3]
	else:
		c = random.choice(candidate)
		Attempt += c
		cur = [c] + cur[:3]
print(Attempt)
