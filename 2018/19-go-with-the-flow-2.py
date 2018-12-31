#!/usr/bin/env python3

r2 = 0
r3 = 0

r2 += 2
r2 *= r2
r2 *= 19
r2 *= 11

r3 += 8
r3 *= 22
r3 += 16

r2 += r3

r3 = 27
r3 *= 28
r3 += 29
r3 *= 30
r3 *= 14
r3 *= 32

r2 += r3

lst = [i for i in range(1, r2 + 1) if r2 % i == 0]

r0 = sum(lst)

print(r0)
