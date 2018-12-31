#!/usr/bin/env python3

import sys
import re

import functools

import unittest


def calc(data):
    lst = re.compile(r'[\s\n,]+').split(data)

    result = functools.reduce(
        lambda x, y:
            x + (int(y[1:]) if y[0] == '+' else - int(y[1:])),
        lst, 0)

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = "+1, -2, +3, +1"

        self.assertEqual(calc(data), 3)

    def test_1(self):
        data = "+1, +1, +1"

        self.assertEqual(calc(data), 3)

    def test_2(self):
        data = "+1, +1, -2"

        self.assertEqual(calc(data), 0)

    def test_3(self):
        data = "-1, -2, -3"

        self.assertEqual(calc(data), -6)


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = ''.join(data).rstrip()

    v = calc(data)

    print(v)
