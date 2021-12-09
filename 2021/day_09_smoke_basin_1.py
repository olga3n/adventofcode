#!/usr/bin/env python3

import sys
from typing import List


def risk_level(data: List[List[str]]) -> int:
    result = 0

    max_row = len(data)
    max_col = len(data[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            min_adj = min([
                data[i + ii][j + jj]
                for ii, jj in {(0, -1), (-1, 0), (0, 1), (1, 0)}
                if 0 <= i + ii < max_row and 0 <= j + jj < max_col
            ])
            if data[i][j] < min_adj:
                result += int(data[i][j]) + 1

    return result


class TestClass():

    def test_1(self):
        data = [
            '2199943210',
            '3987894921',
            '9856789892',
            '8767896789',
            '9899965678',
        ]

        assert risk_level(data) == 15


def main():
    data = [x.strip() for x in sys.stdin]
    result = risk_level(data)
    print(result)


if __name__ == '__main__':
    main()
