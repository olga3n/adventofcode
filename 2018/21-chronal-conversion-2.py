#!/usr/bin/env python3


def part(r5):
    r3 = r5 | 65536
    r5 = 521363

    while True:
        r4 = r3 & 255
        r5 = r4 + r5
        r5 &= 16777215
        r5 *= 65899
        r5 &= 16777215
        if 256 > r3:
            break
        else:
            r4 = 0
            while True:
                r2 = r4 + 1
                r2 *= 256
                if r2 > r3:
                    break
                r4 += 1
            r3 = r4

    return r5


lst = []
r5 = 0

while True:
    r5 = part(r5)
    if r5 not in lst:
        lst.append(r5)
    else:
        break

print(lst[-1])
