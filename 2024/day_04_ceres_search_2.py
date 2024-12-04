#!/usr/bin/env python3

import sys


DIRS = (
    ((1, 1), (-1, -1)),
    ((1, -1), (-1, 1)),
)


def xmas_count(lines: list[str]) -> int:
    result = 0
    candidates = []

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'A':
                candidates.append((i, j))

    for i, j in candidates:
        cnt = 0

        for diff_1, diff_2 in DIRS:
            i0 = i + diff_1[0]
            j0 = j + diff_1[1]

            i1 = i + diff_2[0]
            j1 = j + diff_2[1]

            if not (0 <= i0 < len(lines) and 0 <= j0 < len(lines[0])):
                continue

            if not (0 <= i1 < len(lines) and 0 <= j1 < len(lines[0])):
                continue

            if lines[i0][j0] == 'M' and lines[i1][j1] == 'S':
                cnt += 1
            elif lines[i0][j0] == 'S' and lines[i1][j1] == 'M':
                cnt += 1

        if cnt == 2:
            result += 1

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
    assert 9 == xmas_count(lines)


def main():
    lines = sys.stdin.readlines()
    result = xmas_count(lines)
    print(result)


if __name__ == '__main__':
    main()
