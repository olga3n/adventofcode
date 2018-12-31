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


def process(data):
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

    max_r = 0
    max_point = None

    for item in points:
        if item[3] > max_r:
            max_r = item[3]
            max_point = item

    result = 0

    for item in points:
        if dist_m(max_point, item) <= max_r:
            result += 1

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            pos=<0,0,0>, r=4
            pos=<1,0,0>, r=1
            pos=<4,0,0>, r=3
            pos=<0,2,0>, r=1
            pos=<0,5,0>, r=3
            pos=<0,0,3>, r=1
            pos=<1,1,1>, r=1
            pos=<1,1,2>, r=1
            pos=<1,3,1>, r=1
        """).rstrip().split('\n')

        self.assertEqual(process(data), 7)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = process(data)

    print(v)
