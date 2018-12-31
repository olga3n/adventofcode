#!/usr/bin/env python3

import sys
import re

import unittest


def process_node(lst, curr_ind, curr_sum):
    child_count = lst[curr_ind]
    meta_count = lst[curr_ind + 1]

    curr_ind += 2

    for i in range(child_count):
        curr_ind, part_sum = process_node(lst, curr_ind, 0)

        curr_sum += part_sum

    for j in range(meta_count):
        curr_sum += lst[curr_ind]
        curr_ind += 1

    return curr_ind, curr_sum


def process(data):

    data = re.compile(r'\D+').split(data)
    data = [int(x) for x in data if len(x)]

    curr_ind = 0
    curr_sum = 0

    curr_ind, result = process_node(data, curr_ind, curr_sum)

    return result


class TestMethods(unittest.TestCase):

    def test_1(self):
        data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

        self.assertEqual(process(data), 138)


if __name__ == '__main__':
    data = ''.join(sys.stdin.readlines()).rstrip()

    v = process(data)

    print(v)
