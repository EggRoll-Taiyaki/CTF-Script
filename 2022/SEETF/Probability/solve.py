from pwn import *

import random
from time import time
from mersenne import *
import os

def conn():

    r = remote("fun.chall.seetf.sg", 30001)
    return r

def get_outputs(r):

    outputs = []

    my_sum = 0

    while True:
        r.recvuntil("You draw a [")
        _ = r.recvline().decode().strip().split("].")[0]
        my_sum += float(_)
        outputs += [float(_)]
        if my_sum >= 1:
            return outputs, 0
        if my_sum < 0.5:
            r.sendline(b"h")
        else:
            break

    r.sendline(b"s")

    dealer_sum = 0

    while dealer_sum <= my_sum:
        r.recvuntil("Dealer draws a [")
        _ = r.recvline().decode().strip().split("].")[0]
        dealer_sum += float(_)
        outputs += [float(_)]

    if dealer_sum >= 1:
        return outputs, 1
    else:
        return outputs, 0

def dp(future_outputs):

    L = len(future_outputs)
    win_loss = [0 for i in range(L)]
    h = [0 for i in range(L)]
    bust = [0 for i in range(L)]

    for start in range(L - 50, -1, -1):

        best_h = 0
        max_win_loss = -1000
        check = 0

        ### Take r_{start}, r_{start + 1}, ..., r_{end}
        for my_end in range(start, start + 50):

            my_sum = sum(future_outputs[start: my_end + 1])

            if my_sum >= 1:
                if win_loss[my_end + 1] - 1 > max_win_loss:
                    max_win_loss = win_loss[my_end + 1] - 1
                    best_h = my_end - start
                    check = 1
                break

            dealer_end = my_end + 1
            dealer_sum = 0
            while dealer_sum <= my_sum:                
                dealer_sum += future_outputs[dealer_end]
                dealer_end += 1
            
            if dealer_sum >= 1:
                if win_loss[dealer_end] + 1 > max_win_loss:
                    max_win_loss = win_loss[dealer_end] + 1
                    best_h = my_end - start
            else:
                if win_loss[dealer_end] - 1 > max_win_loss:
                    max_win_loss = win_loss[dealer_end] - 1
                    best_h = my_end - start

        win_loss[start] = max_win_loss
        h[start] = best_h
        bust[start] = check

    return win_loss, h, bust

def solve(r, fake_r, goal):

    future_outputs = [fake_r.random() for i in range(10000)]

    _, h, bust = dp(future_outputs)

    print(_[0])

    win, loss = 0, 0
    start = 0

    while True:

        ### Take r_{start}, r_{start + 1}, ..., r_{end}
        my_end = start + h[start]
        my_sum = sum(future_outputs[start: my_end + 1])

        for j in range(h[start]):
            r.sendline(b"h")

        if my_sum >= 1:
            loss += 1            
            start = my_end + 1
            continue

        dealer_end = my_end + 1
        dealer_sum = 0
        while dealer_sum <= my_sum:                
            dealer_sum += future_outputs[dealer_end]
            dealer_end += 1
            
        if dealer_sum >= 1:
            win += 1
        else:
            loss += 1
    
        if bust[start] == 0:
            r.sendline(b"s")
                
        start = dealer_end

        if (win + loss) % 10 == 0:
            print(f"{win}-{loss}")
            
        if win >= goal:
            break

    return

r = conn()
outputs = []
Round = 0
luck = 0
while len(outputs) < 624:
    Round += 1
    _ = get_outputs(r)
    outputs += _[0]
    luck += _[1]

print(f"Already win {luck} times :p")

print(f"Using {Round} Rounds to Get Enough Outputs!")
L = len(outputs)
print(f"and there are totally {L} random outputs ... @@")

b = BreakerPy()
mt = b.state_recovery_rand(outputs)

print("Finish State Recovery")

### Check
fake_r = MTpython() 
fake_r.MT = mt
fake_outputs = [fake_r.random() for i in range(L)]

for i in range(L):
    assert fake_outputs[i] == outputs[i]

print("Pass Checking")

solve(r, fake_r, 800 - luck)
r.interactive()
r.close()
