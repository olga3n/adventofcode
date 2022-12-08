#!/usr/bin/env python3

import sys
from typing import List
from collections import namedtuple


def visible_trees(data: List[str]) -> int:
    rows, cols = len(data), len(data[0])

    Dp = namedtuple('Dp', ['left', 'right', 'top', 'bottom'])
    dp = Dp([], [], [], [])

    for row in range(rows):
        dp.left.append(['0'] * cols)
        dp.right.append(['0'] * cols)
        dp.top.append(['0'] * cols)
        dp.bottom.append(['0'] * cols)

    for row in range(rows):
        for col in range(cols):
            col_l, col_r = col, cols - col - 1
            row_t, row_b = row, rows - row - 1

            dp.left[row][col_l] = max(
                dp.left[row][col_l - 1], data[row][col_l]
            ) if col_l > 0 else data[row][col_l]

            dp.right[row][col_r] = max(
                dp.right[row][col_r + 1], data[row][col_r]
            ) if col_r < cols - 1 else data[row][col_r]

            dp.top[row_t][col] = max(
                dp.top[row_t - 1][col], data[row_t][col]
            ) if row_t > 0 else data[row_t][col]

            dp.bottom[row_b][col] = max(
                dp.bottom[row_b + 1][col], data[row_b][col]
            ) if row_b < rows - 1 else data[row_b][col]

    result = 0

    for row in range(rows):
        for col in range(cols):
            if row == 0 or col == 0 or row == rows - 1 or col == cols - 1:
                result += 1
            elif (dp.left[row][col - 1] < data[row][col] or
                    dp.right[row][col + 1] < data[row][col] or
                    dp.top[row - 1][col] < data[row][col] or
                    dp.bottom[row + 1][col] < data[row][col]):
                result += 1

    return result


def test_visible_trees():
    data = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390'
    ]

    assert visible_trees(data) == 21


def main():
    data = [line.rstrip() for line in sys.stdin]
    result = visible_trees(data)
    print(result)


if __name__ == '__main__':
    main()
