from main import *
from random import *

inv_SUB_KEY = [
	SUB_KEY.index(i) for i in range(256)
]

reverse_add = {
	(3 * i) & 0xFF : i for i in range(256)
}

def equal(block1, block2):

	for i in range(4):
		for j in range(4):
			if block1[i][j] != block2[i][j]:
				return False
	return True

def check():

	rand_mat = [[89, 252, 192, 128], [235, 234, 167, 20], [26, 144, 156, 109], [82, 250, 31, 124]]	

	tmp = [[89, 252, 192, 128], [235, 234, 167, 20], [26, 144, 156, 109], [82, 250, 31, 124]]

	sub(tmp)
	inv_sub(tmp)
	assert equal(rand_mat, tmp), "inv_sub failed"

	xor(tmp)
	inv_xor(tmp)	
	assert equal(rand_mat, tmp), "inv_xor failed"

	add(tmp)
	inv_add(tmp)
	assert equal(rand_mat, tmp), "inv_add failed"

	swap(tmp)
	inv_swap(tmp)
	assert equal(rand_mat, tmp), "inv_swap failed"

	round(tmp)
	inv_round(tmp)
	assert equal(rand_mat, tmp), "inv_round failed"

def inv_xor(block):

	for i in range(3, -1, -1):
		for j in range(3, -1, -1):
			block[i][j] ^= block[(i + 2) % 4][(j + 1) % 4]
	
def inv_add(block):
	
	for i in range(3, -1, -1):
		for j in range(3, -1, -1):
			if i == 0:
				block[i][j] = reverse_add[block[i][j]]
			else:
				block[i][j] -= 2 * block[(i * 3) % 4][(i + j) % 4]
				block[i][j] &= 0xFF

def inv_sub(block):

	for i in range(4):
		for j in range(4):
			block[i][j] = inv_SUB_KEY[block[i][j]]

def inv_rotate(row):

	row[0], row[1], row[2], row[3] = row[1], row[2], row[3], row[0]

def inv_swap(block):

	s = 0
	for i in range(4):
		for j in range(4):
			s += block[i][j]
    
	if (s % 2): transpose(block)

	for i in range(2, -1, -1):
		for j in range(3, -1, -1):
			ii = i % 4
			jj = (j + 3) % 4
			block[i][j], block[ii][jj] = block[ii][jj], block[i][j]

	inv_rotate(block[3]); inv_rotate(block[3]); inv_rotate(block[3]);
	inv_rotate(block[2])
	inv_rotate(block[1]); inv_rotate(block[1]); inv_rotate(block[1])
	inv_rotate(block[0]); inv_rotate(block[0])

	block[2], block[0] = block[0], block[2]
	block[2], block[1] = block[1], block[2]
	block[3], block[0] = block[3], block[0]
	block[0], block[1] = block[1], block[0]
	block[3], block[2] = block[2], block[3]
	block[0], block[2] = block[2], block[0]

def inv_round(block):

        inv_xor(block)
        inv_swap(block)
        inv_add(block)
        inv_sub(block)

def decryptBlock(block):

	mat = [[block[i * 4 + j] for j in range(4)] for i in range(4)]
	for _ in range(30):
		inv_round(mat)
	return [mat[i][j] for i in range(4) for j in range(4)]	

def decrypt(enc):

	msg = []
	for i in range(0, len(enc), 16):
		msg += decryptBlock(enc[i : i + 16])
	return bytes(msg)

check()

enc = bytes.fromhex("1333087ba678a43ecc697247e2dde06e1d78cb20d8d9326e7c4b01674a46647674afc1e7edd930828e40af60b998b4500361e3a2a685c5515babe4e9ff1fe882")
FLAG = decrypt(enc)
print(FLAG)


