#!/usr/bin/env python3

import sys

import numpy as np

import unittest
import textwrap


def dist_m(p1, p2):
    return \
        abs(p1[0] - p2[0]) + \
        abs(p1[1] - p2[1]) + \
        abs(p1[2] - p2[2]) + \
        abs(p1[3] - p2[3])


def parse_data(data):
    points = np.full((len(data), 5), np.inf)

    for i in range(len(data)):
        prs = [int(x) for x in data[i].split(',')]

        points[i][0], points[i][1], \
            points[i][2], points[i][3] = prs

        points[i][4] = i

    return points


def constellations(data, radius=3):
    points = parse_data(data)

    points_ind = {}
    constellations_dict = {}

    for ind, p in enumerate(points):
        p_ind = \
            abs(p[0]) + abs(p[1]) + abs(p[2]) + abs(p[3])

        constellation = int(p[4])
        lst = [ind]

        for prev_ind in points_ind:
            if abs(prev_ind - p_ind) <= radius:

                for p_ind_0 in points_ind[prev_ind]:
                    if dist_m(points[p_ind_0], p) <= radius:
                        prev_constellation = int(points[p_ind_0][4])

                        if prev_constellation in constellations_dict:
                            for p_ind_i in \
                                    constellations_dict[prev_constellation]:
                                points[p_ind_i][4] = constellation

                            lst += constellations_dict[prev_constellation]

                            constellations_dict.pop(prev_constellation, None)

        constellations_dict[constellation] = lst

        if p_ind not in points_ind:
            points_ind[p_ind] = [ind]
        else:
            points_ind[p_ind].append(ind)

    result = len(constellations_dict.keys())

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            0,0,0,0
            3,0,0,0
            0,3,0,0
            0,0,3,0
            0,0,0,3
            0,0,0,6
            9,0,0,0
            12,0,0,0
            """).rstrip().split("\n")

        self.assertEqual(constellations(data), 2)

    def test_1(self):
        data = textwrap.dedent("""\
            0,0,0,0
            3,0,0,0
            0,3,0,0
            0,0,3,0
            0,0,0,3
            0,0,0,6
            9,0,0,0
            12,0,0,0
            6,0,0,0
            """).rstrip().split("\n")

        self.assertEqual(constellations(data), 1)

    def test_2(self):
        data = textwrap.dedent("""\
            -1,2,2,0
            0,0,2,-2
            0,0,0,-2
            -1,2,0,0
            -2,-2,-2,2
            3,0,2,-1
            -1,3,2,2
            -1,0,-1,0
            0,2,1,-2
            3,0,0,0
            """).rstrip().split("\n")

        self.assertEqual(constellations(data), 4)

    def test_3(self):
        data = textwrap.dedent("""\
            1,-1,0,1
            2,0,-1,0
            3,2,-1,0
            0,0,3,1
            0,0,-1,-1
            2,3,-2,0
            -2,2,0,0
            2,-2,0,-1
            1,-1,0,-1
            3,2,0,2
            """).rstrip().split("\n")

        self.assertEqual(constellations(data), 3)

    def test_4(self):
        data = textwrap.dedent("""\
            1,-1,-1,-2
            -2,-2,0,1
            0,2,1,3
            -2,3,-2,1
            0,2,3,-2
            -1,-1,1,-2
            0,-2,-1,0
            -2,2,3,-1
            1,2,2,0
            -1,-2,0,-2
            """).rstrip().split("\n")

        self.assertEqual(constellations(data), 8)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = constellations(data)

    print(v)
