#!/usr/bin/env python3

import sys
from typing import Iterable


def cube_free_sides(data: Iterable[str]) -> int:
    cubes = {tuple(map(int, line.split(','))) for line in data}
    diffs = {
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    }

    result = 0

    for cube_x, cube_y, cube_z in cubes:
        for diff_x, diff_y, diff_z in diffs:
            next_cube = (
                cube_x + diff_x,
                cube_y + diff_y,
                cube_z + diff_z
            )
            if next_cube not in cubes:
                result += 1

    return result


def test_cube_free_sides_0():
    data = [
        '1,1,1',
        '2,1,1'
    ]

    assert cube_free_sides(data) == 10


def test_cube_free_sides_1():
    data = [
        '2,2,2',
        '1,2,2',
        '3,2,2',
        '2,1,2',
        '2,3,2',
        '2,2,1',
        '2,2,3',
        '2,2,4',
        '2,2,6',
        '1,2,5',
        '3,2,5',
        '2,1,5',
        '2,3,5'
    ]

    assert cube_free_sides(data) == 64


def main():
    data = sys.stdin
    result = cube_free_sides(data)
    print(result)


if __name__ == '__main__':
    main()
