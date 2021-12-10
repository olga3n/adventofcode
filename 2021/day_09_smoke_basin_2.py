#!/usr/bin/env python3

import sys
from typing import List, Tuple


def basin_size(data: List[str], point: Tuple[int, int]) -> int:
    max_row = len(data)
    max_col = len(data[0])

    used = [[0] * max_col for row in range(max_row)]

    size = 0
    q = [point]

    while len(q):
        i, j = q.pop()

        if used[i][j] == 1:
            continue

        used[i][j] = 1
        size += 1

        for ii, jj in {(0, -1), (-1, 0), (0, 1), (1, 0)}:
            if not 0 <= i + ii < max_row or not 0 <= j + jj < max_col:
                continue
            if data[i + ii][j + jj] == '9':
                continue
            if used[i + ii][j + jj] == 1:
                continue
            q.append((i + ii, j + jj))

    return size


def risk_level(data: List[str]) -> int:
    low_points = []

    max_row = len(data)
    max_col = len(data[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            min_adj = min([
                data[i + ii][j + jj]
                for ii, jj in {(0, -1), (-1, 0), (0, 1), (1, 0)}
                if 0 <= i + ii < max_row and 0 <= j + jj < max_col
            ])
            if data[i][j] < min_adj and data[i][j] != '9':
                low_points.append((i, j))

    sizes = sorted(
        [basin_size(data, point) for point in low_points],
        reverse=True
    )

    return sizes[0] * sizes[1] * sizes[2]


class TestClass():

    def test_1(self):
        data = [
            '2199943210',
            '3987894921',
            '9856789892',
            '8767896789',
            '9899965678',
        ]

        assert risk_level(data) == 1134


def main():
    data = [x.strip() for x in sys.stdin]
    result = risk_level(data)
    print(result)


if __name__ == '__main__':
    main()
