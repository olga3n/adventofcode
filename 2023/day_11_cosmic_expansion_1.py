#!/usr/bin/env python3

import sys
from typing import List, Set


def expanding_rows(data: List[str]) -> Set[int]:
    rows = set()
    for i, line in enumerate(data):
        if all(ch == '.' for ch in line):
            rows.add(i)
    return rows


def expanding_cols(data: List[str]) -> Set[int]:
    cols = set()
    for i in range(len(data[0])):
        if all(data[j][i] == '.' for j in range(len(data))):
            cols.add(i)
    return cols


def sum_lengths(data: List[str]) -> int:
    rows = expanding_rows(data)
    cols = expanding_cols(data)

    galaxies = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != '#':
                continue
            galaxies.append((i, j))

    result = 0

    for g1, (x1, y1) in enumerate(galaxies):
        for g2, (x2, y2) in enumerate(galaxies):
            if g2 >= g1:
                continue

            dx = max(x1, x2) - min(x1, x2)
            dy = max(y1, y2) - min(y1, y2)

            for i in range(min(x1, x2), max(x1, x2)):
                if i in rows:
                    dx += 1

            for j in range(min(y1, y2), max(y1, y2)):
                if j in cols:
                    dy += 1

            result += dx + dy

    return result


def test_sum_lengths():
    data = [
        '...#......',
        '.......#..',
        '#.........',
        '..........',
        '......#...',
        '.#........',
        '.........#',
        '..........',
        '.......#..',
        '#...#.....',
    ]
    assert sum_lengths(data) == 374


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = sum_lengths(data)
    print(result)


if __name__ == '__main__':
    main()
