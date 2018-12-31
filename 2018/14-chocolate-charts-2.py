#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest


def process(pattern, first, second):
    scoreboard = np.zeros(100_500_000)

    scoreboard[0] = first
    scoreboard[1] = second

    N = len(pattern)

    n1 = 0
    n2 = 1

    last = 1

    result = 2
    break_flag = False

    while True:
        new_vals = int(scoreboard[n1] + scoreboard[n2])
        new_vals = str(new_vals)

        for new_val in new_vals:
            last += 1

            scoreboard[last] = int(new_val)

            if last > N and str(int(scoreboard[last])) == pattern[-1]:
                tail = ''.join(
                    [str(int(x)) for x in scoreboard[last + 1 - N:last + 1]])

                if tail == pattern:
                    break_flag = True
                    result = last + 1 - N
                    break

        if break_flag:
            break

        n1 = (n1 + int(scoreboard[n1]) + 1) % (last + 1)
        n2 = (n2 + int(scoreboard[n2]) + 1) % (last + 1)

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        s = '51589'

        self.assertEqual(process(s, 3, 7), 9)

    def test_1(self):
        s = '01245'

        self.assertEqual(process(s, 3, 7), 5)

    def test_2(self):
        s = '92510'

        self.assertEqual(process(s, 3, 7), 18)

    def test_3(self):
        s = '59414'

        self.assertEqual(process(s, 3, 7), 2018)


if __name__ == '__main__':
    data = ''.join(sys.stdin.readlines()).rstrip()

    v = process(data, 3, 7)

    print(v)
