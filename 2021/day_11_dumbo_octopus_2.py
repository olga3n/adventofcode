#!/usr/bin/env python3

import sys
from typing import List


def one_step(data: List[List[int]]) -> int:

    for i in range(len(data)):
        data[i] = [x + 1 for x in data[i]]

    lst = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] > 9:
                lst.append((i, j))

    while len(lst):
        i, j = lst.pop()

        for ii in {-1, 0, 1}:
            for jj in {-1, 0, 1}:
                if ii == 0 and jj == 0:
                    continue
                if not 0 <= i + ii < len(data):
                    continue
                if not 0 <= j + jj < len(data[0]):
                    continue
                if data[i + ii][j + jj] < 10:
                    data[i + ii][j + jj] += 1
                    if data[i + ii][j + jj] > 9:
                        lst.append((i + ii, j + jj))
    result = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] > 9:
                data[i][j] = 0
                result += 1

    return result


def all_flashes(data: List[str]) -> int:
    table = [list(map(int, list(row))) for row in data]

    step = 0

    while True:
        step += 1
        if one_step(table) == len(table) * len(table[0]):
            break

    return step


class TestClass():

    def test_1(self):
        data = [
            '5483143223',
            '2745854711',
            '5264556173',
            '6141336146',
            '6357385478',
            '4167524645',
            '2176841721',
            '6882881134',
            '4846848554',
            '5283751526',
        ]

        assert all_flashes(data) == 195


def main():
    data = [x.strip() for x in sys.stdin]
    result = all_flashes(data)
    print(result)


if __name__ == '__main__':
    main()
