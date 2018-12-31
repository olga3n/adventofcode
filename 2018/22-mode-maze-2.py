#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap

import heapq


def build_maze(data):
    d = int(data[0].split(' ')[1])
    target = data[1].split(' ')[1].split(',')

    target_x = int(target[0])
    target_y = int(target[1])

    XN = target_x + 100
    YN = target_y + 100

    m_e = np.zeros((YN + 1, XN + 1))
    m_t = np.zeros((YN + 1, XN + 1))

    for y in range(YN + 1):
        for x in range(XN + 1):
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

    return m_t, (target_y, target_x)


def neighbours_dist(m, p, tool, d):
    y, x = p

    coord_lst = []

    if y > 0:
        coord_lst.append((y - 1, x))

    if x > 0:
        coord_lst.append((y, x - 1))

    if y < m.shape[0] - 1:
        coord_lst.append((y + 1, x))

    if x < m.shape[1] - 1:
        coord_lst.append((y, x + 1))

    reg_type = m[y][x]

    dist_lst = []

    for point in coord_lst:
        n_reg_type = m[point[0]][point[1]]

        for new_tool in ['torch', 'gear', 'neither']:
            dist = d

            if new_tool != tool:
                if reg_type == 0 and new_tool in ['torch', 'gear']:
                    dist += 7
                elif reg_type == 1 and new_tool in ['gear', 'neither']:
                    dist += 7
                elif reg_type == 2 and new_tool in ['torch', 'neither']:
                    dist += 7
                else:
                    dist = np.inf

            if n_reg_type == 0 and new_tool in ['torch', 'gear']:
                dist += 1
            elif n_reg_type == 1 and new_tool in ['gear', 'neither']:
                dist += 1
            elif n_reg_type == 2 and new_tool in ['torch', 'neither']:
                dist += 1
            else:
                dist = np.inf

            if dist < np.inf:
                dist_lst.append((dist, point, new_tool))

    return dist_lst


def shortest_path(m, target):

    YN, XN = m.shape

    d = np.full((YN, XN, 3), np.inf)
    old = np.full((YN, XN, 3), 0)

    nodes = []
    heapq.heappush(nodes, (0, (0, 0), 'torch'))

    d[0][0][0] = 0

    while len(nodes):
        dist, point, tool = heapq.heappop(nodes)

        tool_ind = ['torch', 'gear', 'neither'].index(tool)

        if old[point[0]][point[1]][tool_ind] != 0:
            continue

        old[point[0]][point[1]][tool_ind] = 1

        if point == target:
            break

        lst = neighbours_dist(m, point, tool, dist)

        for item in lst:

            if item[1] == target:
                if item[2] != 'torch':
                    item = (item[0] + 7, item[1], item[2])

            new_dist, new_point, new_tool = item

            y, x = new_point

            new_tool_ind = ['torch', 'gear', 'neither'].index(tool)

            if old[new_point[0]][new_point[1]][new_tool_ind] != 0:
                continue

            if new_tool == 'torch':
                d[y][x][0] = min(new_dist, d[y][x][0])
            elif new_tool == 'gear':
                d[y][x][1] = min(new_dist, d[y][x][1])
            elif new_tool == 'neither':
                d[y][x][2] = min(new_dist, d[y][x][2])

            heapq.heappush(nodes, item)

    return int(min(d[target[0]][target[1]]))


def process(data):

    m, target = build_maze(data)

    result = shortest_path(m, target)

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            depth: 510
            target: 10,10
        """).rstrip().split('\n')

        self.assertEqual(process(data), 45)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = process(data)

    print(v)
