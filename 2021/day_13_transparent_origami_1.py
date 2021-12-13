#!/usr/bin/env python3

import sys
from typing import List


def one_fold(data: List[List[int]], axis: int, value: int) -> List[List[int]]:
    max_row, max_col = len(data), len(data[0])

    if axis == 0:
        new_data = [[0] * max_col for row in range(value + 1)]

        for i in range(value + 1):
            for j in range(max_col):
                new_data[i][j] = data[i][j]

        for i in range(value + 1, max_row):
            for j in range(max_col):
                new_data[len(new_data) - (i - value) - 1][j] |= data[i][j]

    elif axis == 1:
        new_data = [[0] * (value + 1) for row in range(max_row)]

        for i in range(max_row):
            for j in range(value + 1):
                new_data[i][j] = data[i][j]

        for i in range(max_row):
            for j in range(value + 1, max_col):
                new_data[i][len(new_data[0]) - (j - value) - 1] |= data[i][j]

    return new_data


def first_fold(data: List[str]) -> int:

    max_row, max_col = 0, 0
    pos_lst = []
    folds = []

    for line in data:
        if ',' in line:
            pos = tuple(map(int, line.split(',')))
            max_col = max(max_col, pos[0])
            max_row = max(max_row, pos[1])
            pos_lst.append(pos)
        elif 'fold' in line:
            prs = line.split('=')
            axis = 1 if prs[0][-1] == 'x' else 0
            folds.append((axis, int(prs[1])))

    table = [[0] * (max_col + 1) for row in range(max_row + 1)]

    for pos in pos_lst:
        table[pos[1]][pos[0]] = 1

    axis, value = folds[0]

    new_table = one_fold(table, axis, value)

    return sum([sum(row) for row in new_table])


class TestClass():

    def test_1(self):
        data = [
            '6,10',
            '0,14',
            '9,10',
            '0,3',
            '10,4',
            '4,11',
            '6,0',
            '6,12',
            '4,1',
            '0,13',
            '10,12',
            '3,4',
            '3,0',
            '8,4',
            '1,10',
            '2,14',
            '8,10',
            '9,0',
            '',
            'fold along y=7',
            'fold along x=5',
        ]

        assert first_fold(data) == 17


def main():
    data = [x.strip() for x in sys.stdin]
    result = first_fold(data)
    print(result)


if __name__ == '__main__':
    main()
