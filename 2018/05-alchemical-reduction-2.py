#!/usr/bin/env python3

import sys

import collections

import unittest


def test_pair(a, b):
    if a.lower() == b.lower():
        if a == a.lower() and b == b.upper():
            return True
        elif a == a.upper() and b == b.lower():
            return True
        else:
            return False
    else:
        return False


def reduction(data):
    st = collections.deque()

    for ch in data:
        if len(st) == 0:
            st.append(ch)
        else:
            if len(st):
                top_ch = st.pop()
                test_flag = test_pair(top_ch, ch)

                if not test_flag:
                    st.append(top_ch)
                    st.append(ch)

    return st


def reduction_len(data):
    r = reduction(data)

    return len(r)


def min_reduction_len(data):
    min_len = len(data)

    for del_char in 'abcdefghijklmnopqrstuvwxyz':
        new_data = ''

        for ch in data:
            if ch.lower() != del_char:
                new_data += ch

        curr_len = reduction_len(new_data)

        if curr_len < min_len:
            min_len = curr_len

    return min_len


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = "dabAcCaCBAcCcaDA"

        self.assertEqual(min_reduction_len(data), 4)


if __name__ == '__main__':
    data = ''.join(sys.stdin.readlines()).rstrip()

    v = min_reduction_len(data)

    print(v)
