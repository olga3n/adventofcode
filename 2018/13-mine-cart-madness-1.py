#!/usr/bin/env python3

import sys
import re

import heapq

import unittest
import textwrap


def parse(track):
    carts = []

    for j, item in enumerate(track):
        for m in re.finditer(r'[\^v<>]', item):

            col = m.span()[0]
            row = j

            heapq.heappush(carts, (row, col, m.group(), 0))

            if track[row][col] in ['^', 'v']:
                track[row] = track[row][:col] + '|' + track[row][col + 1:]

            if track[row][col] in ['<', '>']:
                track[row] = track[row][:col] + '-' + track[row][col + 1:]

    return track, carts


def process(data):

    track, carts = parse(data)

    x, y = -1, -1

    directions = {
        '^': {0: '<', 1: '^', 2: '>'},
        'v': {0: '>', 1: 'v', 2: '<'},
        '<': {0: 'v', 1: '<', 2: '^'},
        '>': {0: '^', 1: '>', 2: 'v'},
    }

    turns = {
        '^': {'/': '>', '\\': '<'},
        'v': {'/': '<', '\\': '>'},
        '<': {'/': 'v', '\\': '^'},
        '>': {'/': '^', '\\': 'v'},
    }

    n = len(carts)
    crash_status = False

    while True:
        new_carts = []

        for i in range(n):
            row, col, direction, state = heapq.heappop(carts)

            if direction == '^':
                row -= 1
            elif direction == 'v':
                row += 1
            elif direction == '<':
                col -= 1
            elif direction == '>':
                col += 1

            pos = [(x[0], x[1]) for x in carts] + \
                [(x[0], x[1]) for x in new_carts]

            if (row, col) in pos:
                crash_status = True

                x, y = col, row
            elif track[row][col] == '+':
                new_direction = directions[direction][state]
                new_state = (state + 1) % 3

                heapq.heappush(new_carts, (row, col, new_direction, new_state))
            elif track[row][col] in ['/', '\\']:
                new_direction = turns[direction][track[row][col]]

                heapq.heappush(new_carts, (row, col, new_direction, state))
            else:
                heapq.heappush(new_carts, (row, col, direction, state))

        carts = new_carts

        if crash_status:
            break

    return x, y


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent(r"""
            |
            v
            |
            |
            |
            ^
            |
        """).split("\n")

        data = [x for x in data if len(x)]

        x, y = process(data)

        self.assertEqual(x, 0)
        self.assertEqual(y, 3)

    def test_1(self):
        data = textwrap.dedent(r"""
            /->-\
            |   |  /----\
            | /-+--+-\  |
            | | |  | v  |
            \-+-/  \-+--/
              \------/
        """).split("\n")

        data = [x for x in data if len(x)]

        x, y = process(data)

        self.assertEqual(x, 7)
        self.assertEqual(y, 3)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    x, y = process(data)

    print('%s,%s' % (x, y))
