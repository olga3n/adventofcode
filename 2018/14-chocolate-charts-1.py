#!/usr/bin/env python3

import sys
import re

import unittest


class Node(object):

    def __init__(self, val, ind, left, right):
        self.ind = ind
        self.val = val

        self.left = left
        self.right = right


def process(steps, first, second, N=10):

    n1 = Node(first, 0, None, None)
    n2 = Node(second, 1, None, None)

    n1.left = n2
    n1.right = n2

    n2.left = n1
    n2.right = n1

    last = n2

    while True:
        new_vals = str(n1.val + n2.val)

        for new_val in new_vals:
            n_new = Node(int(new_val), last.ind + 1, last, last.right)

            last.right = n_new
            last = n_new

        if last.ind >= steps + N - 1:
            while last.ind != steps + N - 1:
                last = last.left

            break

        n1_steps = n1.val + 1
        n2_steps = n2.val + 1

        for i in range(n1_steps):
            n1 = n1.right

        for i in range(n2_steps):
            n2 = n2.right

    result = ''

    for i in range(N):
        result = str(last.val) + result
        last = last.left

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        steps = 9

        self.assertEqual(process(steps, 3, 7), '5158916779')

    def test_1(self):
        steps = 5

        self.assertEqual(process(steps, 3, 7), '0124515891')

    def test_2(self):
        steps = 18

        self.assertEqual(process(steps, 3, 7), '9251071085')

    def test_3(self):
        steps = 2018

        self.assertEqual(process(steps, 3, 7), '5941429882')


if __name__ == '__main__':
    data = int(''.join(sys.stdin.readlines()).rstrip())

    v = process(data, 3, 7)

    print(v)
