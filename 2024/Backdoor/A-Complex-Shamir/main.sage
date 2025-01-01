from sage.all import *
from Crypto.Util.number import *
from flag import flag 
import random

precision = 1000
degree = 68

R = RealField(prec=precision)
C = ComplexField(prec=precision)

theta = R(acos(R.random_element()))
base = C(exp(I * theta))

print(base)

samples = [bytes_to_long(flag)]

for i in range(degree):
    samples.append(random.randint(1, 2 ** 256))

random.shuffle(samples)

def eval_polynomial(x):
    evaluate = 0
    for i in range(degree + 1):
        evaluate += samples[i] * (x ** i) 
    return evaluate 

print(f"degree = {degree} however {degree + 1} tries is all you get! (the plus one because im generous haha)")
for i in range(degree + 1):
    x = int(input(f"Input {i}: "))
    if x <= 0:
        print("Maybe one day...")
        exit(0)
    print(C(base ** eval_polynomial(x)))
