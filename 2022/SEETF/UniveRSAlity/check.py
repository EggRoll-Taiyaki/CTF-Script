import math
from Crypto.Util.number import isPrime
from params import *

print(str(float(math.pi)))
print(str(float(p)))
print(str(float(math.e)))
print(str(float(q)))

assert isPrime(p) and p.bit_length() == 128
assert str(float(math.pi)) in str(float(p))
assert isPrime(q) and q.bit_length() == 128
assert str(float(math.e)) in str(float(q))

