#!/usr/bin/env python3

import sys
from typing import List


def check_acess(
    lines: List[str], row: int, col: int, roll: str, max_rolls=3,
) -> bool:
    adj_rolls = 0

    for di in {-1, 0, 1}:
        for dj in {-1, 0, 1}:
            if di == dj == 0:
                continue

            new_row = row + di
            new_col = col + dj

            if not 0 <= new_row < len(lines):
                continue
            if not 0 <= new_col < len(lines[0]):
                continue

            if lines[new_row][new_col] == roll:
                adj_rolls += 1

    return adj_rolls <= max_rolls


def accessible_rolls(lines: List[str], roll='@') -> int:
    result = 0

    for row, line in enumerate(lines):
        for col, symbol in enumerate(line):
            if symbol == roll and check_acess(lines, row, col, roll=roll):
                result += 1

    return result


def test_accessible_rolls():
    lines = [
        '..@@.@@@@.',
        '@@@.@.@.@@',
        '@@@@@.@.@@',
        '@.@@@@..@.',
        '@@.@@@@.@@',
        '.@@@@@@@.@',
        '.@.@.@.@@@',
        '@.@@@.@@@@',
        '.@@@@@@@@.',
        '@.@.@@@.@.',
    ]
    assert 13 == accessible_rolls(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = accessible_rolls(lines)
    print(result)


if __name__ == '__main__':
    main()
