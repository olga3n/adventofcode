#!/usr/bin/env python3

import sys
from typing import List


def cycle_shift(matrix: List[List[str]]):
    for i in range(1, len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'O':
                continue
            for ii in range(i - 1, -1, -1):
                if matrix[ii][j] != '.':
                    break
                matrix[ii + 1][j], matrix[ii][j] = '.', 'O'

    for j in range(1, len(matrix[0])):
        for i in range(len(matrix)):
            if matrix[i][j] != 'O':
                continue
            for jj in range(j - 1, -1, -1):
                if matrix[i][jj] != '.':
                    break
                matrix[i][jj + 1], matrix[i][jj] = '.', 'O'

    for i in range(len(matrix) - 1, -1, -1):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'O':
                continue
            for ii in range(i + 1, len(matrix)):
                if matrix[ii][j] != '.':
                    break
                matrix[ii - 1][j], matrix[ii][j] = '.', 'O'

    for j in range(len(matrix[0]) - 1, -1, -1):
        for i in range(len(matrix)):
            if matrix[i][j] != 'O':
                continue
            for jj in range(j + 1, len(matrix[0])):
                if matrix[i][jj] != '.':
                    break
                matrix[i][jj - 1], matrix[i][jj] = '.', 'O'


def calc_score(matrix: List[List[str]]) -> int:
    score = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'O':
                score += len(matrix) - i

    return score


def total_load(data: List[str], cnt: int = 1000000000) -> int:
    matrix = [list(line) for line in data]

    store = {}
    values = []
    new_cnt = cnt - 1

    for i in range(cnt):
        cycle_shift(matrix)

        view = ''.join(''.join(row) for row in matrix)

        if view not in store:
            store[view] = i
        else:
            values = values[store[view]:]
            new_cnt = cnt - store[view] - 1
            break

        values.append(calc_score(matrix))

    return values[new_cnt % len(values)]


def test_total_load():
    data = [
        'O....#....',
        'O.OO#....#',
        '.....##...',
        'OO.#O....O',
        '.O.....O#.',
        'O.#..O.#.#',
        '..O..#O..O',
        '.......O..',
        '#....###..',
        '#OO..#....',
    ]
    assert total_load(data) == 64


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = total_load(data)
    print(result)


if __name__ == '__main__':
    main()
