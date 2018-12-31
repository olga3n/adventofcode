#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def parse_points(data):
    points = np.zeros((len(data), 3))

    max_x = 0
    min_x = 0

    max_y = 0
    min_y = 0

    for i, item in enumerate(data):
        prs = re.compile(r'\D+').split(item)

        x = int(prs[0])
        y = int(prs[1])

        points[i][0] = x
        points[i][1] = y

        min_x = min(min_x, x)
        max_x = max(max_x, x)

        min_y = min(min_y, y)
        max_y = max(max_y, y)

    min_x -= 1
    max_x += 1

    min_y -= 1
    max_y += 1

    return points, min_x, max_x, min_y, max_y


def calc(points, offset_x, offset_y, xn, yn):
    m = np.full((xn, yn, 2), -1)

    for ind, item in enumerate(points):
        xi = int(item[0]) + offset_x
        yi = int(item[1]) + offset_y

        if m[xi][yi][0] != -1:
            points[m[xi][yi][0]][2] -= 1

        m[xi][yi][0] = ind
        m[xi][yi][1] = 0

        points[ind][2] += 1

        for i in range(xn):
            for j in range(yn):
                d = abs(i - xi) + abs(j - yi)

                if d < m[i][j][1] or m[i][j][1] == -1:

                    if m[i][j][1] != -1 and m[i][j][0] != -1:
                        points[m[i][j][0]][2] -= 1

                    m[i][j][0] = ind
                    m[i][j][1] = d

                    points[ind][2] += 1

                elif d > 0 and d == m[i][j][1] and m[i][j][0] != -1:
                    points[m[i][j][0]][2] -= 1

                    m[i][j][0] = -1

    for i in range(xn):
        for j in range(yn):
            if ((i == 0 or i == xn - 1) or (j == 0 or j == yn - 1)) and \
                    m[i][j][0] != -1:
                points[m[i][j][0]][2] = -1

    max_val = 0
    max_p = 0

    for p in points:
        if p[2] > max_val:
            max_val = int(p[2])
            max_p = p

    return max_val


def largest_area(data):
    points, min_x, max_x, min_y, max_y = parse_points(data)

    offset_x = - min_x
    offset_y = - min_y

    xn = max_x - min_x
    yn = max_y - min_y

    result = calc(points, offset_x, offset_y, xn, yn)

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            1, 1
            1, 6
            8, 3
            3, 4
            5, 5
            8, 9
            """).split("\n")

        data = [x for x in data if len(x)]

        self.assertEqual(largest_area(data), 17)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = largest_area(data)

    print(v)
