#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def parse_line(line):
    prs = re.findall(r'[xy]=[\d\.]+', line)

    y_coord = [
        v.split('=')[1].split('..')
        for v in prs if 'y' in v][0]

    x_coord = [
        v.split('=')[1].split('..')
        for v in prs if 'x' in v][0]

    y_coord = list(map(int, y_coord))
    x_coord = list(map(int, x_coord))

    if len(y_coord) == 1:
        y_coord += y_coord

    if len(x_coord) == 1:
        x_coord += x_coord

    return y_coord, x_coord


def build_map(clay_data, water_data):
    clay_coord = np.zeros((len(clay_data), 4))
    water_coord = np.zeros((len(water_data), 4))

    min_x, min_y = np.inf, np.inf
    max_x, max_y = -1, -1

    for ind, item in enumerate(clay_data):
        y_coord, x_coord = parse_line(item)

        clay_coord[ind][0], clay_coord[ind][1] = y_coord
        clay_coord[ind][2], clay_coord[ind][3] = x_coord

        min_x = min(min_x, x_coord[0])
        min_y = min(min_y, y_coord[0])

        max_x = max(max_x, x_coord[1])
        max_y = max(max_y, y_coord[1])

    border = min_y

    for ind, item in enumerate(water_data):
        y_coord, x_coord = parse_line(item)

        water_coord[ind][0], water_coord[ind][1] = y_coord
        water_coord[ind][2], water_coord[ind][3] = x_coord

        min_x = min(min_x, x_coord[0])
        min_y = min(min_y, y_coord[0])

        max_x = max(max_x, x_coord[1])
        max_y = max(max_y, y_coord[1])

    border -= min_y

    min_x -= 1
    max_x += 1

    m = []
    for row in range(max_y - min_y + 1):
        m.append('.' * (max_x - min_x + 1))

    for item in clay_coord:
        for y in range(int(item[0] - min_y), int(item[1] - min_y + 1)):
            clay = '#' * int(item[3] - item[2] + 1)

            l1 = int(item[2] - min_x)
            r = l1 + len(clay)

            m[y] = m[y][:l1] + clay + m[y][r:]

    start_points = []

    for item in water_coord:
        for y in range(int(item[0] - min_y), int(item[1] - min_y + 1)):
            clay = '|' * int(item[3] - item[2] + 1)

            l2 = int(item[2] - min_x - 1)
            r = l2 + len(clay)

            m[y] = m[y][:l2] + clay + m[y][r:]

            start_points.append((y, l2))

    return m, start_points, border


def insert_substr(m, pos, substr):
    row, col = pos

    m[row] = m[row][:col] + substr + m[row][col + len(substr):]


def spread_down(m, pos):
    row, col = pos

    while True:
        if row == len(m):
            break

        if m[row][col] in '.|':
            insert_substr(m, (row, col), '|')
        else:
            break

        row += 1

    return (row - 1, col)


def spread_up(m, pos):
    pos_lst = []

    row, col = pos

    while True:
        curr_row, curr_col = row, col

        while True:
            if curr_col < 0:
                break
            if not (curr_row < len(m) - 1 and
                    m[curr_row + 1][curr_col] in '#~' and
                    m[curr_row][curr_col] in '.|'):
                break
            curr_col -= 1

        left = curr_col + 1

        curr_row, curr_col = row, col

        while True:
            if curr_col == len(m[row]):
                break
            if not (curr_row < len(m) - 1 and
                    m[curr_row + 1][curr_col] in '#~' and
                    m[curr_row][curr_col] in '.|'):
                break
            curr_col += 1

        right = curr_col - 1

        if left > 0 and m[curr_row][left - 1] == '#' and \
                right < len(m[curr_row]) - 1 and m[curr_row][right + 1] == '#':
            insert_substr(m, (curr_row, left), '~' * (right - left + 1))
        else:
            insert_substr(m, (curr_row, left), '|' * (right - left + 1))

            if left > 0 and m[curr_row][left - 1] != '#':
                pos_lst.append((curr_row, left - 1))

            if right < len(m[curr_row]) - 1 and m[curr_row][right + 1] != '#':
                pos_lst.append((curr_row, right + 1))

            break

        row -= 1

        if row < 0:
            break

    return pos_lst


def spread_water(m, pos):
    pos_lst = [pos]

    while True:
        new_pos_lst = []

        for pos in pos_lst:
            if pos[0] < len(m) - 1:
                pos = spread_down(m, pos)
                new_pos_lst += spread_up(m, pos)

        if len(new_pos_lst) == 0:
            break

        pos_lst = list(set(new_pos_lst))


def calc_tiles(clay_data, water_data):

    m, start_points, border = build_map(clay_data, water_data)

    for pos in start_points:
        spread_water(m, pos)

    result = 0

    for ind, row in enumerate(m):
        if ind >= border:
            result += len(re.findall(r'[~|]', row))

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        clay_data = textwrap.dedent("""\
            x=495, y=2..7
            y=7, x=495..501
            x=501, y=3..7
            x=498, y=2..4
            x=506, y=1..2
            x=498, y=10..13
            x=504, y=10..13
            y=13, x=498..504
        """).rstrip().split('\n')

        water_data = textwrap.dedent("""\
            x=500, y=0
        """).rstrip().split('\n')

        self.assertEqual(calc_tiles(clay_data, water_data), 57)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    clay_data = [x.rstrip() for x in data]

    water_data = textwrap.dedent("""\
        x=500, y=0
    """).rstrip().split('\n')

    v = calc_tiles(clay_data, water_data)

    print(v)
