#!/usr/bin/env python3

import sys

from enum import Enum
from typing import Iterable


class SideType(Enum):
    UP_HOR = 1
    DOWN_HOR = 2
    LEFT_VER = 3
    RIGHT_VER = 4


DIRS = (
    ((-1, 0), SideType.UP_HOR),
    ((1, 0), SideType.DOWN_HOR),
    ((0, -1), SideType.LEFT_VER),
    ((0, 1), SideType.RIGHT_VER),
)

CORNERS = (
    {SideType.UP_HOR, SideType.LEFT_VER},
    {SideType.UP_HOR, SideType.RIGHT_VER},
    {SideType.DOWN_HOR, SideType.LEFT_VER},
    {SideType.DOWN_HOR, SideType.RIGHT_VER},
)

DIAG_ADJ = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)


def gen_adj(
    lines: list[str], i: int, j: int,
) -> Iterable[tuple[tuple[int, int], SideType]]:

    for (dx, dy), side_type in DIRS:
        ii = i + dx
        jj = j + dy

        if not 0 <= ii < len(lines):
            continue

        if not 0 <= jj < len(lines[0]):
            continue

        if lines[i][j] != lines[ii][jj]:
            continue

        yield ((ii, jj), side_type)


def corners(
    lines: list[str], i: int, j: int, curr_sides: set[SideType],
) -> int:

    result = 0

    for corner in CORNERS:
        if corner.issubset(curr_sides):
            result += 1

    check_internal = []

    for index in range(len(CORNERS)):
        if len(CORNERS[index].intersection(curr_sides)) == 0:
            check_internal.append(DIAG_ADJ[index])

    for dx, dy in check_internal:
        ii = i + dx
        jj = j + dy

        if not 0 <= ii < len(lines):
            continue

        if not 0 <= jj < len(lines[0]):
            continue

        if lines[i][j] != lines[ii][jj]:
            result += 1

    return result


def area_score(
    lines: list[str], visited: list[list[bool]], i: int, j: int,
) -> int:

    stack = [(i, j)]
    sides = 0
    area = 0

    while stack:
        i, j = stack.pop()

        if visited[i][j]:
            continue

        visited[i][j] = True
        curr_sides = {
            SideType.UP_HOR,
            SideType.DOWN_HOR,
            SideType.LEFT_VER,
            SideType.RIGHT_VER,
        }

        for (ii, jj), side_type in gen_adj(lines, i, j):
            stack.append((ii, jj))
            curr_sides.remove(side_type)

        sides += corners(lines, i, j, curr_sides)
        area += 1

    return area * sides


def total_price(lines: list[str]) -> int:
    visited = []

    for line in lines:
        visited.append([False] * len(line))

    result = 0

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if visited[i][j]:
                continue
            result += area_score(lines, visited, i, j)

    return result


def test_total_price_0():
    lines = [
        'AAAA',
        'BBCD',
        'BBCC',
        'EEEC',
    ]
    assert 80 == total_price(lines)


def test_total_price_1():
    lines = [
        'OOOOO',
        'OXOXO',
        'OOOOO',
        'OXOXO',
        'OOOOO',
    ]
    assert 436 == total_price(lines)


def test_total_price_2():
    lines = [
        'RRRRIICCFF',
        'RRRRIICCCF',
        'VVRRRCCFFF',
        'VVRCCCJFFF',
        'VVVVCJJCFE',
        'VVIVCCJJEE',
        'VVIIICJJEE',
        'MIIIIIJJEE',
        'MIIISIJEEE',
        'MMMISSJEEE',
    ]
    assert 1206 == total_price(lines)


def test_total_price_3():
    lines = [
        'EEEEE',
        'EXXXX',
        'EEEEE',
        'EXXXX',
        'EEEEE',
    ]
    assert 236 == total_price(lines)


def test_total_price_4():
    lines = [
        'AAAAAA',
        'AAABBA',
        'AAABBA',
        'ABBAAA',
        'ABBAAA',
        'AAAAAA',
    ]
    assert 368 == total_price(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = total_price(lines)
    print(result)


if __name__ == '__main__':
    main()
