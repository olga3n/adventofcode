#!/usr/bin/env python3

import sys
import re


def inv_pow(x, m):
    return pow(x, m - 2, m)


def shuffle_card(stages, cards_count, shuffle_count, card_pos):
    a = 1
    b = 0

    for stage in stages:
        ai, bi = stage()

        a = (a * ai) % cards_count
        b = (ai * b + bi) % cards_count

    an = pow(a, shuffle_count, cards_count)
    bn = b * (1 - an) * inv_pow(1 - a, cards_count)

    card = ((card_pos - bn) * inv_pow(an, cards_count)) % cards_count

    return card


def stage_new_stack():
    return (-1, -1)


def stage_cut(value):
    return (1, -value)


def stage_increment(value):
    return (value, 0)


def parse_input(data):
    data = [x.strip() for x in data if len(x.strip())]

    stages = []

    for line in data:
        m1 = re.match(r'deal into new stack', line)
        m2 = re.match(r'cut (.+)', line)
        m3 = re.match(r'deal with increment (.+)', line)

        if m1:
            stages.append(stage_new_stack)
        elif m2:
            v = int(m2[1])
            stages.append(lambda v=v: stage_cut(v))
        elif m3:
            v = int(m3[1])
            stages.append(lambda v=v: stage_increment(v))

    return stages


if __name__ == '__main__':
    data = sys.stdin.readlines()

    stages = parse_input(data)

    cards_count = 119315717514047
    shuffle_count = 101741582076661
    card_pos = 2020

    result = shuffle_card(stages, cards_count, shuffle_count, card_pos)

    print(result)
