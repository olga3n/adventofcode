#!/usr/bin/env python3

import sys
from typing import Iterable, Tuple, Optional


def parse_data(
    data: Iterable[str]
) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
    for line in data:
        left, right = line.split(' @ ')
        left = list(map(int, left.split(', ')))
        right = list(map(int, right.split(', ')))
        yield ((left[0], left[1]), (left[0] + right[0], left[1] + right[1]))


def line_coeffs(
    line: Tuple[Tuple[int, int], Tuple[int, int]]
) -> Optional[Tuple[float, float]]:
    x1, y1 = line[0]
    x2, y2 = line[1]

    if x1 != x2:
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        return (a, b)


def find_intersection(
    line_1: Tuple[Tuple[int, int], Tuple[int, int]],
    line_2: Tuple[Tuple[int, int], Tuple[int, int]]
) -> Optional[Tuple[float, float]]:
    coeffs_1 = line_coeffs(line_1)
    coeffs_2 = line_coeffs(line_2)

    if coeffs_1 and coeffs_2:
        a1, b1 = coeffs_1
        a2, b2 = coeffs_2

        if a1 != a2:
            x = (b2 - b1) / (a1 - a2)
            y = a1 * x + b1
            return (x, y)

    if coeffs_1 and not coeffs_2:
        a, b = coeffs_1
        x = line_2[0]
        y = a * x + b
        return (x, y)

    if coeffs_2 and not coeffs_1:
        a, b = coeffs_2
        x = line_1[0]
        y = a * x + b
        return (x, y)


def check_direction(
    line: Tuple[Tuple[int, int], Tuple[int, int]],
    point: Tuple[int, int]
) -> bool:
    x0, y0 = point

    x1, y1 = line[0]
    x2, y2 = line[1]

    one = (x2 >= x1 and x0 >= x1) or (x2 <= x1 and x0 <= x1)
    two = (y2 >= y1 and y0 >= y1) or (y2 <= y1 and y0 <= y1)

    return one and two


def intersections(data: Iterable[str], test_area: Tuple[int, int]) -> int:
    lines = list(parse_data(data))
    result = 0

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            point = find_intersection(lines[i], lines[j])
            if point is None:
                continue
            one = test_area[0] <= point[0] <= test_area[1]
            two = test_area[0] <= point[1] <= test_area[1]
            if not one or not two:
                continue
            one = check_direction(lines[i], point)
            two = check_direction(lines[j], point)
            if not one or not two:
                continue
            result += 1

    return result


def test_intersections():
    data = [
        '19, 13, 30 @ -2,  1, -2',
        '18, 19, 22 @ -1, -1, -2',
        '20, 25, 34 @ -2, -2, -4',
        '12, 31, 28 @ -1, -2, -1',
        '20, 19, 15 @  1, -5, -3',
    ]
    assert intersections(data, (7, 27)) == 2


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    test_area = (200000000000000, 400000000000000)
    result = intersections(data, test_area)
    print(result)


if __name__ == '__main__':
    main()
