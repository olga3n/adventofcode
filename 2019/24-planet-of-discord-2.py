#!/usr/bin/env python3

import sys


def adj_bugs(state, level, i, j):
    bugs = 0

    if i == 0 and level + 1 in state and state[level + 1][1][2] == '#':
        bugs += 1

    if i > 0 and state[level][i - 1][j] == '#':
        bugs += 1

    if i < len(state[level]) - 1 and state[level][i + 1][j] == '#':
        bugs += 1

    if i == len(state[level]) - 1 and level + 1 in state and \
            state[level + 1][3][2] == '#':
        bugs += 1

    if j == 0 and level + 1 in state and state[level + 1][2][1] == '#':
        bugs += 1

    if j > 0 and state[level][i][j - 1] == '#':
        bugs += 1

    if j < len(state[level][i]) - 1 and state[level][i][j + 1] == '#':
        bugs += 1

    if j == len(state[level][i]) - 1 and level + 1 in state and \
            state[level + 1][2][3] == '#':
        bugs += 1

    if (i, j) == (1, 2) and level - 1 in state:
        bugs += sum([1 for tile in state[level - 1][0] if tile == '#'])

    if (i, j) == (2, 1) and level - 1 in state:
        bugs += sum([1 for line in state[level - 1] if line[0] == '#'])

    if (i, j) == (2, 3) and level - 1 in state:
        bugs += sum([1 for line in state[level - 1] if line[-1] == '#'])

    if (i, j) == (3, 2) and level - 1 in state:
        bugs += sum([1 for tile in state[level - 1][-1] if tile == '#'])

    return bugs


def next_state(state):
    min_level = min(state.keys())
    max_level = max(state.keys())

    empty_level = ['.....'] * 5

    state[min_level - 1] = empty_level
    state[max_level + 1] = empty_level

    new_state = {}

    for level in state.keys():
        new_tiles = []

        for i in range(len(state[level])):
            new_line = ''

            for j in range(len(state[level][i])):
                if i == 2 and j == 2:
                    new_line += '?'
                    continue

                if state[level][i][j] == '#':
                    if adj_bugs(state, level, i, j) != 1:
                        new_line += '.'
                    else:
                        new_line += '#'
                elif state[level][i][j] == '.':
                    if 1 <= adj_bugs(state, level, i, j) <= 2:
                        new_line += '#'
                    else:
                        new_line += '.'

            new_tiles.append(new_line)

        new_state[level] = new_tiles

    return new_state


def bugs_count(init_state, iterations):
    state = {}
    state[0] = init_state

    for i in range(iterations):
        state = next_state(state)

    bugs = 0

    for level, tiles in state.items():
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if tiles[i][j] == '#':
                    bugs += 1

    return bugs


class TestClass:
    def test_bugs_count_0(self):
        data = [
            '....#',
            '#..#.',
            '#.?##',
            '..#..',
            '#....']

        assert bugs_count(data, 10) == 99


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.strip() for x in data if len(x.strip())]

    data[2] = data[2][:2] + '?' + data[2][-2:]

    result = bugs_count(data, 200)

    print(result)
