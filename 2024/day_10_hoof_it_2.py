#!/usr/bin/env python3

import sys
from typing import Iterable


DIFFS = (
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
)


def is_valid_step(
    lines: list[str], pos_1: tuple[int, int], pos_2: tuple[int, int],
) -> bool:
    symbol_1 = lines[pos_1[0]][pos_1[1]]
    symbol_2 = lines[pos_2[0]][pos_2[1]]
    return int(symbol_1) + 1 == int(symbol_2)


def gen_adj(
    lines: list[str], pos: tuple[int, int],
) -> Iterable[tuple[int, int]]:

    for diff in DIFFS:
        next_pos = (
            pos[0] + diff[0],
            pos[1] + diff[1],
        )

        if not 0 <= next_pos[0] < len(lines):
            continue

        if not 0 <= next_pos[1] < len(lines[0]):
            continue

        if is_valid_step(lines, pos, next_pos):
            yield next_pos


def tails_from_pos(lines: list[str], pos: tuple[int, int]) -> int:
    result = 0
    stack = [pos]

    while len(stack) > 0:
        pos = stack.pop()

        if lines[pos[0]][pos[1]] == '9':
            result += 1

        for next_pos in gen_adj(lines, pos):
            stack.append(next_pos)

    return result


def tails_cnt(lines: list[str], start='0') -> int:
    result = 0

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == start:
                result += tails_from_pos(lines, (i, j))

    return result


def test_tails_cnt():
    lines = [
        '89010123',
        '78121874',
        '87430965',
        '96549874',
        '45678903',
        '32019012',
        '01329801',
        '10456732',
    ]
    assert 81 == tails_cnt(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = tails_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()
