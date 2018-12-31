#!/usr/bin/env python3

import sys
import re

import unittest


def calc(lst):
    result = 0

    v = 0
    i = 0

    freq = {}

    freq[0] = 1

    while True:
        item = lst[i]

        if item[0] == '+':
            v += int(item[1:])
        else:
            v -= int(item[1:])

        if v not in freq:
            freq[v] = 1
        else:
            result = v
            break

        i += 1

        i = 0 if i == len(lst) else i

    return result


def process(s):
    lst = re.compile(r'[\s\n,]+').split(s)

    v = calc(lst)

    return v


class TestMethods(unittest.TestCase):

    def test_0(self):
        self.assertEqual(process('+1, -2, +3, +1'), 2)

    def test_1(self):
        self.assertEqual(process('+1, -1'), 0)

    def test_2(self):
        self.assertEqual(process('+3, +3, +4, -2, -4'), 10)

    def test_3(self):
        self.assertEqual(process('-6, +3, +8, +5, -6'), 5)

    def test_4(self):
        self.assertEqual(process('+7, +7, -2, -7, -4'), 14)


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = ''.join(data).rstrip()

    v = process(data)

    print(v)
