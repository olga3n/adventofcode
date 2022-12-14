#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple


def parse_lines(
    data: Iterable[str]
) -> Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]]:

    for line in data:
        points = [
            tuple(map(int, point.split(','))) for point in line.split(' -> ')
        ]
        for i in range(len(points) - 1):
            yield points[i], points[i + 1]


def build_field(
    lines: List[Tuple[Tuple[int, ...], Tuple[int, ...]]]
) -> Tuple[List[List[str]], int]:
    min_col, max_col = 100500, 0
    max_row = 0

    for line in lines:
        for point in line:
            min_col = min(point[0], min_col)
            max_col = max(point[0], max_col)
            max_row = max(point[1], max_row)

    rows = max_row + 1
    cols = max_col - min_col + 1
    shift = min_col

    field = []

    for _ in range(rows):
        field.append(['.'] * cols)

    for line in lines:
        point_1, point_2 = line

        row = point_1[1]
        col1 = min(point_1[0], point_2[0]) - shift
        col2 = max(point_1[0], point_2[0]) - shift

        for col in range(col1, col2 + 1):
            field[row][col] = '#'

        col = point_1[0] - shift
        row1 = min(point_1[1], point_2[1])
        row2 = max(point_1[1], point_2[1])

        for row in range(row1, row2 + 1):
            field[row][col] = '#'

    return field, shift


def max_sand_units(
    data: Iterable[str], sand_pos: Tuple[int, int] = (500, 0)
) -> int:
    lines = list(parse_lines(data))
    field, shift = build_field(lines)
    sand_pos = (sand_pos[1], sand_pos[0] - shift)

    dirs = [(1, 0), (1, -1), (1, 1)]
    result = 0

    while True:
        sand = sand_pos
        flag = True

        while flag:
            flag = False

            for row, col in dirs:
                x, y = sand[0] + row, sand[1] + col
                if not 0 <= x < len(field) or not 0 <= y < len(field[0]):
                    return result
                if field[x][y] == '.':
                    sand = (x, y)
                    flag = True
                    break

        field[sand[0]][sand[1]] = 'o'
        result += 1

    return result


def test_max_sand_units():
    data = [
        '498,4 -> 498,6 -> 496,6',
        '503,4 -> 502,4 -> 502,9 -> 494,9'
    ]

    assert max_sand_units(data) == 24


def main():
    data = sys.stdin
    result = max_sand_units(data)
    print(result)


if __name__ == '__main__':
    main()
