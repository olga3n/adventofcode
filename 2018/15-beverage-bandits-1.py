#!/usr/bin/env python3

import sys
import re

import heapq
import collections

import numpy as np

import logging

import unittest
import textwrap


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_neighbours(data, row, col, group):
    lst = []

    if row > 0 and data[row - 1][col] != '#':
        lst.append((row - 1, col))

    if col > 0 and data[row][col - 1] != '#':
        lst.append((row, col - 1))

    if col < len(data[row]) - 1 and data[row][col + 1] != '#':
        lst.append((row, col + 1))

    if row < len(data) - 1 and data[row + 1][col] != '#':
        lst.append((row + 1, col))

    free_lst = []
    vict_lst = []

    for x in lst:
        if data[x[0]][x[1]] != '.':
            if data[x[0]][x[1]] != group:
                vict_lst.append(x)
        else:
            free_lst.append(x)

    return free_lst, vict_lst


def bfs_dist(data, row, col, group):
    dist = 100500

    q = collections.deque()
    old_pos = np.zeros((len(data), len(data[0])))

    q.append((row, col, 1))
    old_pos[row][col] = 1

    while len(q):
        curr_row, curr_col, curr_dist = q.popleft()

        f_lst, v_lst = get_neighbours(data, curr_row, curr_col, group)

        if len(v_lst):
            dist = curr_dist + 1
            break

        for pos in f_lst:
            if old_pos[pos[0]][pos[1]] == 0:
                q.append((pos[0], pos[1], curr_dist + 1))
                old_pos[pos[0]][pos[1]] = 1

    return dist


def battle(data, attack_power=3, start_points=200):
    units = []
    game_round = 0
    scores = {}

    for row, line in enumerate(data):
        logging.info(line)

        for player in re.finditer('[GE]', line):

            col = player.span()[0]
            unit_id = len(units)

            unit = (row, col, player.group(), unit_id)
            scores[(row, col)] = [start_points, unit_id]

            heapq.heappush(units, unit)

    while True:
        logging.info("ROUND %s" % game_round)
        logging.info("UNITS: %s" % units)
        logging.info("SCORES: %s" % scores)

        for row, line in enumerate(data):
            logging.info(line)

        n = len(units)

        new_units = []

        no_vict_flag = False

        for i in range(n):
            row, col, group, unit_id = heapq.heappop(units)

            if (row, col) not in scores or scores[(row, col)][1] != unit_id:
                continue

            score = scores[(row, col)][0]

            vict_lst = [x for x in units + new_units
                        if x[2] != group and (x[0], x[1]) in scores and
                        scores[(x[0], x[1])][1] == x[3] and
                        scores[(x[0], x[1])][0] > 0]

            if len(vict_lst) == 0:
                no_vict_flag = True
                break

            f_lst, v_lst = get_neighbours(data, row, col, group)

            if len(v_lst) == 0 and len(f_lst):
                min_dist = 100500
                min_pos = (-1, -1)

                for pos in f_lst:
                    dist = bfs_dist(data, pos[0], pos[1], group)

                    if dist < min_dist:
                        min_dist = dist
                        min_pos = pos

                if min_pos != (-1, -1):
                    new_row, new_col = min_pos

                    data[row] = data[row][:col] + '.' + data[row][col + 1:]
                    data[new_row] = data[new_row][:new_col] + group + \
                        data[new_row][new_col + 1:]

                    scores.pop((row, col), None)
                    scores[min_pos] = [score, unit_id]

                    f_lst, v_lst = get_neighbours(
                        data, new_row, new_col, group)

                    row, col = new_row, new_col

            if len(v_lst):
                min_score = scores[v_lst[0]][0]
                vict = v_lst[0]

                for ind in range(1, len(v_lst)):
                    curr_score = scores[v_lst[ind]][0]
                    curr_vict = v_lst[ind]

                    if curr_score < min_score:
                        min_score = curr_score
                        vict = curr_vict

                scores[vict] = [scores[vict][0] - attack_power,
                                scores[vict][1]]

                logging.info("attacked: %s, %s" % (vict[1], vict[0]))

                if scores[vict][0] <= 0:
                    v_row, v_col = vict

                    data[v_row] = data[v_row][:v_col] + '.' + \
                        data[v_row][v_col + 1:]

                    scores.pop(vict, None)

                    logging.info("killed: %s, %s" % (v_row, v_col))

            heapq.heappush(new_units, (row, col, group, unit_id))

        units = new_units

        if no_vict_flag:
            break

        game_round += 1

    result = sum([v[0] for k, v in scores.items() if v[0] > 0])
    result *= game_round

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            #######
            #.G...#
            #...EG#
            #.#.#G#
            #..G#E#
            #.....#
            #######
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 27730)

    def test_1(self):
        data = textwrap.dedent("""\
            #######
            #G..#E#
            #E#E.E#
            #G.##.#
            #...#E#
            #...E.#
            #######
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 36334)

    def test_2(self):
        data = textwrap.dedent("""\
            #######
            #E..EG#
            #.#G.E#
            #E.##E#
            #G..#.#
            #..E#.#
            #######
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 39514)

    def test_3(self):
        data = textwrap.dedent("""\
            #######
            #E.G#.#
            #.#G..#
            #G.#.G#
            #G..#.#
            #...E.#
            #######
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 27755)

    def test_4(self):
        data = textwrap.dedent("""\
            #######
            #.E...#
            #.#..G#
            #.###.#
            #E#G#G#
            #...#G#
            #######
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 28944)

    def test_5(self):
        data = textwrap.dedent("""\
            #########
            #G......#
            #.E.#...#
            #..##..G#
            #...##..#
            #...#...#
            #.G...G.#
            #.....G.#
            #########
        """).split('\n')

        data = [x for x in data if len(x)]

        self.assertEqual(battle(data), 18740)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = battle(data)

    print(v)
