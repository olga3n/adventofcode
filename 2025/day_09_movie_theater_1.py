#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple


def parse_lines(lines: Iterable[str]) -> List[Tuple[int, int]]:
    result = []

    for line in lines:
        x, y = line.rstrip().split(',')
        result.append((int(x), int(y)))

    return result


def largest_area(points: List[Tuple[int, int]]) -> int:
    result = 0

    for i in range(len(points)):
        x1, y1 = points[i]
        for j in range(i + 1, len(points)):
            x2, y2 = points[j]
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
    assert 50 == largest_area(parse_lines(lines))


def main():
    lines = sys.stdin
    result = largest_area(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
