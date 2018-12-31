#!/usr/bin/env python3

import sys
import re

import unittest
import textwrap


def calc_neighbours(data, y, x):
    t_cnt = 0
    l_cnt = 0

    for offset_y in [-1, 0, 1]:
        for offset_x in [-1, 0, 1]:
            if (offset_y or offset_x) and \
                    0 <= y + offset_y < len(data) and \
                    0 <= x + offset_x < len(data[0]):

                if data[y + offset_y][x + offset_x] == '|':
                    t_cnt += 1

                elif data[y + offset_y][x + offset_x] == '#':
                    l_cnt += 1

    return t_cnt, l_cnt


def next_state(data):
    new_data = []

    for y, row in enumerate(data):
        new_row = ''

        for x, v in enumerate(row):
            t_cnt, l_cnt = calc_neighbours(data, y, x)

            new_v = '.'

            if v == '.' and t_cnt >= 3:
                new_v = '|'
            elif v == '|' and l_cnt >= 3:
                new_v = '#'
            elif v == '|':
                new_v = '|'
            elif v == '#' and l_cnt >= 1 and t_cnt >= 1:
                new_v = '#'
            elif v == '#':
                new_v = '.'

            new_row += new_v

        new_data.append(new_row)

    return new_data


def process(data, N=1000000000):

    stat = {}
    results = []

    period = -1

    for i in range(N):

        data = next_state(data)

        t_cnt = 0
        l_cnt = 0

        for row in data:
            t_cnt += len(re.findall(r'[|]', row))
            l_cnt += len(re.findall(r'[#]', row))

        if (t_cnt, l_cnt) in stat and \
                stat[(t_cnt, l_cnt)][1] == data:

            period = i - stat[(t_cnt, l_cnt)][0]
            break

        stat[(t_cnt, l_cnt)] = [i, data.copy()]

        results.append(t_cnt * l_cnt)

    if period != -1:
        ind = len(results) - period + ((N - len(results) - 1) % period)

        result = results[ind]
    else:
        result = results[-1]

    return result


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(data)]

    v = process(data)

    print(v)
