#!/usr/bin/env python3

import sys
from typing import List


def north_shift(matrix: List[List[int]]):
    for i in range(1, len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'O':
                for ii in range(i - 1, -1, -1):
                    if matrix[ii][j] == '.':
                        matrix[ii + 1][j], matrix[ii][j] = '.', 'O'
                    else:
                        break


def total_load(data: List[str]) -> int:
    matrix = [list(line) for line in data]
    north_shift(matrix)
    score = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'O':
                score += len(matrix) - i

    return score


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
    assert total_load(data) == 136


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = total_load(data)
    print(result)


if __name__ == '__main__':
    main()
