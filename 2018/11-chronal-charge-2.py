#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest


def build_grid(serial_number, xn=300, yn=300):
    m = np.zeros((xn, yn))

    for i in range(xn):
        for j in range(yn):
            rack_id = (10 + (i + 1))

            v = (rack_id * (j + 1) + serial_number) * rack_id
            v = str(v)[-3] if len(str(v)) > 2 else ''
            v = int(v) if len(v) and v != '-' else 0

            m[i][j] = v - 5

    return m


def get_top_left(m):
    xn, yn = m.shape

    for i in range(xn):
        for j in range(yn):
            if j > 0:
                m[i][j] += m[i][j - 1]

        if i > 0:
            for j in range(yn):
                m[i][j] += m[i - 1][j]

    x, y, power, size = 0, 0, 0, 1

    for s in range(1, 301):
        for i in range(xn - s + 1):
            for j in range(yn - s + 1):
                power_curr = m[i + s - 1][j + s - 1]

                if i > 0 and j > 0:
                    power_curr += m[i - 1][j - 1]

                if i > 0:
                    power_curr -= m[i - 1][j + s - 1]

                if j > 0:
                    power_curr -= m[i + s - 1][j - 1]

                if power_curr > power:
                    power = power_curr

                    x = i
                    y = j

                    size = s

    return int(x + 1), int(y + 1), int(size), int(power)


def process(serial_number):
    grid = build_grid(serial_number=serial_number)

    x, y, size, power = get_top_left(grid)

    return x, y, size


class TestStringMethods(unittest.TestCase):

    def test_build_grid_0(self):

        serial_number = 8
        grid = build_grid(serial_number=serial_number)

        self.assertEqual(grid[3 - 1][5 - 1], 4)

    def test_build_grid_1(self):

        serial_number = 57
        grid = build_grid(serial_number=serial_number)

        self.assertEqual(grid[122 - 1][79 - 1], -5)

    def test_build_grid_2(self):

        serial_number = 39
        grid = build_grid(serial_number=serial_number)

        self.assertEqual(grid[217 - 1][196 - 1], 0)

    def test_build_grid_3(self):

        serial_number = 71
        grid = build_grid(serial_number=serial_number)

        self.assertEqual(grid[101 - 1][153 - 1], 4)

    def test_process_cell_0(self):

        serial_number = 18
        grid = build_grid(serial_number=serial_number)

        x, y, size, power = get_top_left(grid)

        self.assertEqual(x, 90)
        self.assertEqual(y, 269)

        self.assertEqual(size, 16)

        self.assertEqual(power, 113)

    def test_process_cell_1(self):

        serial_number = 42
        grid = build_grid(serial_number=serial_number)

        x, y, size, power = get_top_left(grid)

        self.assertEqual(x, 232)
        self.assertEqual(y, 251)

        self.assertEqual(size, 12)

        self.assertEqual(power, 119)


if __name__ == '__main__':
    serial_number = int(''.join(sys.stdin.readlines()).rstrip())

    x, y, size = process(serial_number=serial_number)

    print('%s,%s,%s' % (x, y, size))
