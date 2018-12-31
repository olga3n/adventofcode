#!/usr/bin/env python3

import sys
import re

import numpy as np

import copy

import unittest
import textwrap


def parse_data(data):
    points = np.zeros((len(data), 2))
    dt = np.zeros((len(data), 2))

    min_x, min_y = np.inf, np.inf
    max_x, max_y = 0, 0

    for i, item in enumerate(data):
        prs = [x for x in re.compile(r'[, <>]').split(item) if len(x)]

        x = int(prs[1])
        y = int(prs[2])

        dx = int(prs[4])
        dy = int(prs[5])

        points[i][0] = x
        points[i][1] = y

        dt[i][0] = dx
        dt[i][1] = dy

        min_x = min(x, min_x)
        min_y = min(y, min_y)

        max_x = max(x, max_x)
        max_y = max(y, max_y)

    xn = int(max_x - min_x) + 1
    yn = int(max_y - min_y) + 1

    return points, dt, xn, yn, min_x, min_y


def time_for_message(data):
    points, dt, xn, yn, min_x, min_y = parse_data(data)

    last_xn, last_yn = xn, yn
    last_min_x, last_min_y = min_x, min_y

    last_points = copy.deepcopy(points)

    result = 0

    while True:

        min_x, min_y = np.inf, np.inf
        max_x, max_y = 0, 0

        for ind, item in enumerate(points):

            points[ind][0] += dt[ind][0]
            points[ind][1] += dt[ind][1]

            min_x = min(points[ind][0], min_x)
            min_y = min(points[ind][1], min_y)

            max_x = max(points[ind][0], max_x)
            max_y = max(points[ind][1], max_y)

        xn = int(max_x - min_x) + 1
        yn = int(max_y - min_y) + 1

        if (xn > last_xn and yn > last_yn):
            break

        last_xn, last_yn = xn, yn
        last_min_x, last_min_y = min_x, min_y

        last_points = copy.deepcopy(points)

        result += 1

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data_in = textwrap.dedent("""\
                position=< 9,  1> velocity=< 0,  2>
                position=< 7,  0> velocity=<-1,  0>
                position=< 3, -2> velocity=<-1,  1>
                position=< 6, 10> velocity=<-2, -1>
                position=< 2, -4> velocity=< 2,  2>
                position=<-6, 10> velocity=< 2, -2>
                position=< 1,  8> velocity=< 1, -1>
                position=< 1,  7> velocity=< 1,  0>
                position=<-3, 11> velocity=< 1, -2>
                position=< 7,  6> velocity=<-1, -1>
                position=<-2,  3> velocity=< 1,  0>
                position=<-4,  3> velocity=< 2,  0>
                position=<10, -3> velocity=<-1,  1>
                position=< 5, 11> velocity=< 1, -2>
                position=< 4,  7> velocity=< 0, -1>
                position=< 8, -2> velocity=< 0,  1>
                position=<15,  0> velocity=<-2,  0>
                position=< 1,  6> velocity=< 1,  0>
                position=< 8,  9> velocity=< 0, -1>
                position=< 3,  3> velocity=<-1,  1>
                position=< 0,  5> velocity=< 0, -1>
                position=<-2,  2> velocity=< 2,  0>
                position=< 5, -2> velocity=< 1,  2>
                position=< 1,  4> velocity=< 2,  1>
                position=<-2,  7> velocity=< 2, -2>
                position=< 3,  6> velocity=<-1, -1>
                position=< 5,  0> velocity=< 1,  0>
                position=<-6,  0> velocity=< 2,  0>
                position=< 5,  9> velocity=< 1, -2>
                position=<14,  7> velocity=<-2,  0>
                position=<-3,  6> velocity=< 2, -1>
            """).split("\n")

        data_in = [x for x in data_in if len(x)]

        self.assertEqual(time_for_message(data_in), 3)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = time_for_message(data)

    print(v)
