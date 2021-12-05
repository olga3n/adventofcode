#!/usr/bin/env python3

import sys
from typing import List


def overlap_score(data: List[str]) -> int:
    max_row = 0
    max_col = 0

    borders = []

    for line in data:
        p1, p2 = line.split(' -> ')

        col1, row1 = list(map(int, p1.split(',')))
        col2, row2 = list(map(int, p2.split(',')))

        if row1 == row2 or col1 == col2:
            max_col = max(max_col, col1, col2)
            max_row = max(max_row, row1, row2)

            borders.append(((col1, row1), (col2, row2)))

    field = [[0] * (max_col + 1) for _ in range(max_row + 1)]

    for pair in borders:
        point1, point2 = pair

        col1, col2 = min(point1[0], point2[0]), max(point1[0], point2[0])
        row1, row2 = min(point1[1], point2[1]), max(point1[1], point2[1])

        for row in range(row1, row2 + 1):
            for col in range(col1, col2 + 1):
                field[row][col] += 1

    return sum([sum([1 for x in row if x > 1]) for row in field])


class TestClass():

    def test_1(self):
        data = [
            '0,9 -> 5,9',
            '8,0 -> 0,8',
            '9,4 -> 3,4',
            '2,2 -> 2,1',
            '7,0 -> 7,4',
            '6,4 -> 2,0',
            '0,9 -> 2,9',
            '3,4 -> 1,4',
            '0,0 -> 8,8',
            '5,5 -> 8,2',
        ]

        assert overlap_score(data) == 5


def main():
    data = [x.strip() for x in sys.stdin]
    result = overlap_score(data)
    print(result)


if __name__ == '__main__':
    main()
