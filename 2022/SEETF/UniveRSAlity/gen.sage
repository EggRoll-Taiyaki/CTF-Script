p = 314159265358979349999999999999999999999
q = 271828182845904549999999999999999999999

def find_prev_smooth_prime(n):

	while True:
		while n.is_prime() == False:
			n -= 2

		_ = list(factor(n - 1))

		Test = True

		for pp, e in _:
			if pp > 2^30:
				Test = False	

		if Test:
			break
		else:
			n -= 2

	return n

p = find_prev_smooth_prime(p)
q = find_prev_smooth_prime(q)

print(p)
print(q)


