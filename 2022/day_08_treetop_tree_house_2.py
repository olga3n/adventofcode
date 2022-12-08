#!/usr/bin/env python3

import sys
from typing import List
from collections import namedtuple


def visible_trees_max_score(data: List[str]) -> int:
    rows, cols = len(data), len(data[0])

    Dp = namedtuple('Dp', ['left', 'right', 'top', 'bottom'])
    dp = Dp([], [], [], [])

    for row in range(rows):
        dp.left.append([0] * cols)
        dp.right.append([0] * cols)
        dp.top.append([0] * cols)
        dp.bottom.append([0] * cols)

    for row in range(rows):
        left_buf = [cols] * 10
        right_buf = [cols] * 10

        for col in range(cols):
            col_r = cols - col - 1

            dp.left[row][col] = min(
                [x for ind, x in enumerate(left_buf)
                    if ind >= int(data[row][col]) and x < cols] + [col]
            )
            dp.right[row][col_r] = min(
                [x for ind, x in enumerate(right_buf)
                    if ind >= int(data[row][col_r]) and x < cols] + [col]
            )

            for i in range(10):
                if i == int(data[row][col]):
                    left_buf[i] = 1
                else:
                    left_buf[i] += 1

                if i == int(data[row][col_r]):
                    right_buf[i] = 1
                else:
                    right_buf[i] += 1

    for col in range(cols):
        top_buf = [rows] * 10
        bottom_buf = [rows] * 10

        for row in range(rows):
            row_b = rows - row - 1

            dp.top[row][col] = min(
                [x for ind, x in enumerate(top_buf)
                    if ind >= int(data[row][col]) and x < rows] + [row]
            )
            dp.bottom[row_b][col] = min(
                [x for ind, x in enumerate(bottom_buf)
                    if ind >= int(data[row_b][col]) and x < rows] + [row]
            )

            for i in range(10):
                if i == int(data[row][col]):
                    top_buf[i] = 1
                else:
                    top_buf[i] += 1

                if i == int(data[row_b][col]):
                    bottom_buf[i] = 1
                else:
                    bottom_buf[i] += 1

    result = 0

    for row in range(rows):
        for col in range(cols):
            score = (
                dp.left[row][col] *
                dp.right[row][col] *
                dp.top[row][col] *
                dp.bottom[row][col]
            )

            result = max(result, score)

    return result


def test_visible_trees_max_score():
    data = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390'
    ]

    assert visible_trees_max_score(data) == 8


def main():
    data = [line.rstrip() for line in sys.stdin]
    result = visible_trees_max_score(data)
    print(result)


if __name__ == '__main__':
    main()
