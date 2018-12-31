#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def parse_points(lst):
    points = np.zeros((len(lst) * 4, 3))

    X = 0
    Y = 0

    for ind, item in enumerate(lst):
        if len(item):
            prs = re.compile(r'[\D]+').split(item)
            prs = [int(x) for x in prs if len(x)]

            points[ind * 4 + 0][0] = prs[1]
            points[ind * 4 + 0][1] = prs[2]
            points[ind * 4 + 0][2] = 1

            points[ind * 4 + 1][0] = prs[1] + prs[3]
            points[ind * 4 + 1][1] = prs[2]
            points[ind * 4 + 1][2] = -1

            points[ind * 4 + 2][0] = prs[1]
            points[ind * 4 + 2][1] = prs[2] + prs[4]
            points[ind * 4 + 2][2] = -1

            points[ind * 4 + 3][0] = prs[1] + prs[3]
            points[ind * 4 + 3][1] = prs[2] + prs[4]
            points[ind * 4 + 3][2] = 1

            X = max(X, prs[1] + prs[3])
            Y = max(Y, prs[2] + prs[4])

    return points, X, Y


def get_id_without_overlap(lst):
    points, XN, YN = parse_points(lst)

    result = 0

    m = np.zeros((XN + 1, YN + 1))

    for i in range(points.shape[0]):
        p = points[i]
        m[int(p[0])][int(p[1])] += int(p[2])

    for i in range(XN + 1):

        for j in range(YN + 1):
            if j > 0:
                m[i][j] += m[i][j - 1]

        if i > 0:
            for j in range(YN + 1):
                m[i][j] += m[i - 1][j]

    for i in range(XN + 1):
        for j in range(YN + 1):
            if j > 0:
                m[i][j] += m[i][j - 1]

        if i > 0:
            for j in range(YN + 1):
                m[i][j] += m[i - 1][j]

    for ind in range((points.shape[0] // 4)):
        p1 = points[ind * 4 + 0]
        p2 = points[ind * 4 + 1]
        p3 = points[ind * 4 + 2]
        p4 = points[ind * 4 + 3]

        sq1 = (p2[0] - p1[0]) * (p3[1] - p1[1])

        sq2 = \
            m[int(p1[0]) - 1][int(p1[1]) - 1] + \
            m[int(p4[0]) - 1][int(p4[1]) - 1] - \
            m[int(p2[0]) - 1][int(p2[1]) - 1] - \
            m[int(p3[0]) - 1][int(p3[1]) - 1]

        if sq1 != 0 and sq2 == sq1:
            result = ind + 1

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
                #1 @ 1,3: 4x4
                #2 @ 3,1: 4x4
                #3 @ 5,5: 2x2
            """).split("\n")

        data = [x for x in data if len(x)]

        self.assertEqual(get_id_without_overlap(data), 3)


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = get_id_without_overlap(data)

    print(v)
