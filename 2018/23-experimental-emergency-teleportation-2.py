#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def dist_m(p1, p2):
    return \
        abs(p1[0] - p2[0]) + \
        abs(p1[1] - p2[1]) + \
        abs(p1[2] - p2[2])


def parse_data(data):
    points = np.zeros((len(data), 4))

    for i, line in enumerate(data):
        prs = line.split(', ')

        prs[0] = [
            int(x) for x in re.compile(r'[^\-0-9]+').split(prs[0])
            if len(x)]

        prs[1] = [
            int(x) for x in re.compile(r'[^\-0-9]+').split(prs[1])
            if len(x)]

        points[i][0], points[i][1], \
            points[i][2], points[i][3] = prs[0] + prs[1]

    return points


def max_overlap(data):

    points = parse_data(data)

    min_v = np.min(points[:, :-1])
    max_v = np.max(points[:, :-1])

    step = int(max_v - min_v)

    min_0 = int(np.min(points[:, 0]))
    max_0 = int(np.max(points[:, 0]))

    min_1 = int(np.min(points[:, 1]))
    max_1 = int(np.max(points[:, 1]))

    min_2 = int(np.min(points[:, 2]))
    max_2 = int(np.max(points[:, 2]))

    best_point = None
    best_dist = np.inf
    best_overlap = 0

    while step > 0:

        for x in range(min_0, max_0 + 1, step):
            for y in range(min_1, max_1 + 1, step):
                for z in range(min_2, max_2 + 1, step):

                    curr_overlap = 0
                    curr_p = (x, y, z)

                    for p in points:
                        d = dist_m(curr_p, p)

                        if d <= p[-1]:
                            curr_overlap += 1

                    curr_dist = dist_m((0, 0, 0), curr_p)

                    if curr_overlap > best_overlap:
                        best_overlap = curr_overlap
                        best_point = curr_p
                        best_dist = curr_dist

                    elif curr_overlap == best_overlap and \
                            curr_dist < best_dist:
                        best_point = curr_p
                        best_dist = curr_dist

        min_0 = int(best_point[0] - step)
        max_0 = int(best_point[0] + step)

        min_1 = int(best_point[1] - step)
        max_1 = int(best_point[1] + step)

        min_2 = int(best_point[2] - step)
        max_2 = int(best_point[2] + step)

        step //= 2

    return best_dist


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            pos=<10,12,12>, r=2
            pos=<12,14,12>, r=2
            pos=<16,12,12>, r=4
            pos=<14,14,14>, r=6
            pos=<50,50,50>, r=200
            pos=<10,10,10>, r=5
        """).rstrip().split('\n')

        self.assertEqual(max_overlap(data), 36)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = max_overlap(data)

    print(v)
