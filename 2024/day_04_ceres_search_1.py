#!/usr/bin/env python3

import sys


DIRS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
)


def xmas_count(lines: list[str], pattern='XMAS') -> int:
    result = 0
    stack = []

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == pattern[0]:
                for dir_index in range(len(DIRS)):
                    stack.append((i, j, dir_index, 1))

    while len(stack):
        i, j, dir_index, pattern_index = stack.pop()

        new_i = i + DIRS[dir_index][0]
        new_j = j + DIRS[dir_index][1]

        if not (0 <= new_i < len(lines) and 0 <= new_j < len(lines[0])):
            continue

        if lines[new_i][new_j] != pattern[pattern_index]:
            continue

        if pattern_index == len(pattern) - 1:
            result += 1
            continue

        stack.append((new_i, new_j, dir_index, pattern_index + 1))

    return result


def test_xmas_count():
    lines = [
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX',
    ]
    assert 18 == xmas_count(lines)


def main():
    lines = sys.stdin.readlines()
    result = xmas_count(lines)
    print(result)


if __name__ == '__main__':
    main()
