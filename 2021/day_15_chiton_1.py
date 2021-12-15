#!/usr/bin/env python3

import sys
from typing import List


def lowest_risk_path(data: List[str]) -> int:

    table = [[int(x) for x in line] for line in data]
    score = [[100500] * len(line) for line in data]
    used = [[0] * len(line) for line in data]

    candidates = {(0, 0)}
    score[0][0] = 0

    while len(candidates):
        i, j = min(candidates, key=lambda x: score[x[0]][x[1]])

        for ii, jj in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            if not 0 <= i + ii < len(data):
                continue
            if not 0 <= j + jj < len(data[0]):
                continue
            if score[i + ii][j + jj] > score[i][j] + table[i + ii][j + jj]:
                score[i + ii][j + jj] = score[i][j] + table[i + ii][j + jj]
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

        assert lowest_risk_path(data) == 40


def main():
    data = [x.strip() for x in sys.stdin]
    result = lowest_risk_path(data)
    print(result)


if __name__ == '__main__':
    main()
