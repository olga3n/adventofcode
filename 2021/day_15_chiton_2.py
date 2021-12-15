#!/usr/bin/env python3

import sys
from typing import List


def lowest_risk_path(data: List[str], scale: int = 5) -> int:

    table = [[int(x) for x in line] for line in data]

    size_row = len(data) * scale
    size_col = len(data[0]) * scale

    score = [[100500] * size_col for line in range(size_row)]
    used = [[0] * size_col for line in range(size_row)]

    candidates = {(0, 0)}
    score[0][0] = 0

    while len(candidates):
        i, j = min(candidates, key=lambda x: score[x[0]][x[1]])

        for ii, jj in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            if not 0 <= i + ii < size_row:
                continue
            if not 0 <= j + jj < size_col:
                continue
            table_score = (
                (
                    table[(i + ii) % len(table)][(j + jj) % len(table[0])] +
                    (i + ii) // len(table) +
                    (j + jj) // len(table[0]) - 1
                ) % 9 + 1
            )
            if score[i + ii][j + jj] > score[i][j] + table_score:
                score[i + ii][j + jj] = score[i][j] + table_score
            if used[i + ii][j + jj] == 0:
                candidates.add((i + ii, j + jj))

        used[i][j] = 1
        candidates.remove((i, j))

    return score[-1][-1]


class TestClass():

    def test_1(self):
        data = [
            '1163751742',
            '1381373672',
            '2136511328',
            '3694931569',
            '7463417111',
            '1319128137',
            '1359912421',
            '3125421639',
            '1293138521',
            '2311944581',
        ]

        assert lowest_risk_path(data) == 315


def main():
    data = [x.strip() for x in sys.stdin]
    result = lowest_risk_path(data)
    print(result)


if __name__ == '__main__':
    main()
