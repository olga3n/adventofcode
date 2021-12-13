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


def fold(data: List[str]) -> List[List[int]]:

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

    for fold in folds:
        axis, value = fold
        new_table = one_fold(table, axis, value)
        table = new_table

    return new_table


def main():
    data = [x.strip() for x in sys.stdin]
    result = fold(data)

    for row in result:
        print(''.join(['#' if x == 1 else ' ' for x in row]))


if __name__ == '__main__':
    main()
