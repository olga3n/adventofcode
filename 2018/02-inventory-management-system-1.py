#!/usr/bin/env python3

import sys

import unittest
import textwrap


def calc_checksum(lst):
    id2 = 0
    id3 = 0

    for item in lst:
        freq = {}

        twice = 0
        third = 0

        for ch in item:
            if ch not in freq:
                freq[ch] = 1
            else:
                freq[ch] += 1

        for ch in freq.keys():
            if freq[ch] == 2:
                twice = ch

            if freq[ch] == 3:
                third = ch

        if twice != 0:
            id2 += 1

        if third != 0:
            id3 += 1

    return id2 * id3


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
                abcdef
                bababc
                abbcde
                abcccd
                aabcdd
                abcdee
                ababab
            """).split('\n')

        self.assertEqual(calc_checksum(data), 12)


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = calc_checksum(data)

    print(v)
