#!/usr/bin/env python3

import sys
from collections import deque
from typing import List, Tuple

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

ADJ_DICT = {
    '|': {UP, DOWN},
    '-': {LEFT, RIGHT},
    'L': {UP, RIGHT},
    'J': {UP, LEFT},
    '7': {LEFT, DOWN},
    'F': {RIGHT, DOWN},
}


def resolve_start(data: List[str], start) -> Tuple[Tuple[int, int], str]:
    for i, row in enumerate(data):
        j = row.find(start)
        if j > -1:
            ii, jj = i, j
            break

    dirs = set()

    for i_diff, j_diff in (UP, DOWN, LEFT, RIGHT):
        i, j = ii + i_diff, jj + j_diff
        rev_diff_i, rev_diff_j = -i_diff, -j_diff

        if not (0 <= i < len(data) and 0 <= j < len(data[0])):
            continue

        if (rev_diff_i, rev_diff_j) in ADJ_DICT.get(data[i][j], set()):
            dirs.add((i_diff, j_diff))

    for pipe, adj in ADJ_DICT.items():
        one, two = adj
        if one in dirs and two in dirs:
            break

    return (ii, jj), pipe


def max_path_steps(data: List[str], start='S') -> int:
    start_pos, start_pipe = resolve_start(data, start)

    visited = set(start_pos)
    states = [
        ((start_pos[0] + xx, start_pos[1] + yy), 1)
        for xx, yy in ADJ_DICT[start_pipe]
    ]
    q = deque(states)
    max_steps = 1

    while len(q):
        pos, steps = q.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        max_steps = max(max_steps, steps)
        x, y = pos
        for x_diff, y_diff in ADJ_DICT.get(data[x][y], set()):
            i, j = x + x_diff, y + y_diff
            if not (0 <= i < len(data) and 0 <= j < len(data[0])):
                continue
            if data[i][j] == '.' or (i, j) in visited:
                continue
            q.append(((i, j), steps + 1))

    return max_steps


def test_max_path_steps_1():
    data = [
        '.....',
        '.S-7.',
        '.|.|.',
        '.L-J.',
        '.....',
    ]
    assert max_path_steps(data) == 4


def test_max_path_steps_2():
    data = [
        '..F7.',
        '.FJ|.',
        'SJ.L7',
        '|F--J',
        'LJ...',
    ]
    assert max_path_steps(data) == 8


def test_max_path_steps_3():
    data = [
        '7-F7-',
        '.FJ|7',
        'SJLL7',
        '|F--J',
        'LJ.LJ',
    ]
    assert max_path_steps(data) == 8


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = max_path_steps(data)
    print(result)


if __name__ == '__main__':
    main()
