from Crypto.Util.number import bytes_to_long

ct = bytes.fromhex("982e47b0840b47a59c334facab3376a19a1b50ac861f43bdbc2e5bb98b3375a68d3046e8de7d03b4")
prefix = b"grey"

key = bytes([p ^ c for p, c in zip(prefix, ct[:4])])

def decrypt(c):
	return bytes([x ^ y for x, y in zip(c,key)])

flag = b""
for i in range(0, 40, 4):
	flag += decrypt(bytes(ct[i : i + 4]))
print(flag)

