#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def build_maze(data):
    d = int(data[0].split(' ')[1])
    target = data[1].split(' ')[1].split(',')

    target_x = int(target[0])
    target_y = int(target[1])

    m_e = np.zeros((target_y + 1, target_x + 1))
    m_t = np.zeros((target_y + 1, target_x + 1))

    for y in range(target_y + 1):
        for x in range(target_x + 1):
            if (y == 0 and x == 0) or \
                    (y == target_y and x == target_x):
                geo_index = 0
            elif y == 0:
                geo_index = x * 16807
            elif x == 0:
                geo_index = y * 48271
            else:
                geo_index = m_e[y][x - 1] * m_e[y - 1][x]

            er_level = (geo_index + d) % 20183
            reg_type = er_level % 3

            m_e[y][x] = er_level
            m_t[y][x] = reg_type

    return m_t


def process(data):
    m = build_maze(data)

    result = int(sum(sum(m)))

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            depth: 510
            target: 10,10
        """).rstrip().split('\n')

        self.assertEqual(process(data), 114)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = process(data)

    print(v)
