#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple


def parse_lines(lines: Iterable[str]) -> List[Tuple[int, int]]:
    result = []

    for line in lines:
        x, y = line.rstrip().split(',')
        result.append((int(x), int(y)))

    return result


def minimize_coords(
    points: List[Tuple[int, int]],
) -> Tuple[List[int], List[int], List[Tuple[int, int]]]:

    x_set, y_set = set(), set()

    for x, y in points:
        x_set.add(x)
        y_set.add(y)

    x_sorted = sorted(x_set)
    y_sorted = sorted(y_set)

    scaled_points = []

    for x, y in points:
        scaled_x = x_sorted.index(x)
        scaled_y = y_sorted.index(y)
        scaled_points.append((scaled_x, scaled_y))

    return x_sorted, y_sorted, scaled_points


def build_matrix(
    points: List[Tuple[int, int]], rows: int, cols: int,
) -> List[List[str]]:

    matrix = []

    for _ in range(rows):
        matrix.append(['.' for _ in range(cols)])

    for x, y in points:
        matrix[y][x] = '#'

    prev_point = points[-1]

    for next_point in points:
        if prev_point[0] == next_point[0]:
            x = prev_point[0]
            left = min(prev_point[1], next_point[1])
            right = max(prev_point[1], next_point[1])

            for y in range(left, right + 1):
                if matrix[y][x] != '#':
                    matrix[y][x] = 'X'

        if prev_point[1] == next_point[1]:
            y = prev_point[1]
            left = min(prev_point[0], next_point[0])
            right = max(prev_point[0], next_point[0])

            for x in range(left, right + 1):
                if matrix[y][x] != '#':
                    matrix[y][x] = 'X'

        prev_point = next_point

    return matrix


def find_internal(matrix: List[List[str]]) -> Tuple[int, int]:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'X':
                if i + 1 < len(matrix) and matrix[i + 1][j] == '.':
                    return (i + 1, j)

    return (-1, -1)


def fill_internal(matrix: List[List[str]]):
    i, j = find_internal(matrix)
    stack = [(i, j)]

    while len(stack):
        i, j = stack.pop()

        if matrix[i][j] != '.':
            continue

        for di, dj in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
            if not 0 <= i + di < len(matrix):
                continue
            if not 0 <= j + dj < len(matrix[0]):
                continue
            stack.append((i + di, j + dj))

        matrix[i][j] = 'X'


def is_colored_rect(
    matrix: List[List[str]],
    corner_1: Tuple[int, int], corner_2: Tuple[int, int],
) -> bool:

    left_x = min(corner_1[0], corner_2[0])
    right_x = max(corner_1[0], corner_2[0])

    left_y = min(corner_1[1], corner_2[1])
    right_y = max(corner_1[1], corner_2[1])

    for x in range(left_x, right_x + 1):
        for y in range(left_y, right_y + 1):
            if matrix[y][x] == '.':
                return False

    return True


def largest_area(points: List[Tuple[int, int]]) -> int:
    x_sorted, y_sorted, scaled_points = minimize_coords(points)
    matrix = build_matrix(scaled_points, len(y_sorted), len(x_sorted))
    fill_internal(matrix)

    result = 0

    for i in range(len(scaled_points)):
        x1 = x_sorted[scaled_points[i][0]]
        y1 = y_sorted[scaled_points[i][1]]

        for j in range(i + 1, len(scaled_points)):
            if is_colored_rect(matrix, scaled_points[i], scaled_points[j]):
                x2 = x_sorted[scaled_points[j][0]]
                y2 = y_sorted[scaled_points[j][1]]

                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                result = max(result, area)

    return result


def test_largest_area():
    lines = [
        '7,1',
        '11,1',
        '11,7',
        '9,7',
        '9,5',
        '2,5',
        '2,3',
        '7,3',
    ]
    assert 24 == largest_area(parse_lines(lines))


def main():
    lines = sys.stdin
    result = largest_area(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
