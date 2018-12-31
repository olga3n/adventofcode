#!/usr/bin/env python3

import sys

import unittest
import textwrap


def common_letters(lst):
    freq = {}
    result = 0

    for item in lst:
        for i in range(len(item)):
            seq = item[:i] + '_' + item[i + 1:]

            if seq not in freq:
                freq[seq] = 1
            else:
                freq[seq] += 1

    for seq in freq.keys():
        if freq[seq] > 1:
            result = ''.join(seq.split('_'))
            break

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            abcde
            fghij
            klmno
            pqrst
            fguij
            axcye
            wvxyz
        """).split('\n')

        self.assertEqual(common_letters(data), 'fgij')


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = common_letters(data)

    print(v)
