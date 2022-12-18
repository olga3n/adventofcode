#!/usr/bin/env python3

import sys
from collections import deque
from typing import Iterable


def cube_ext_sides(data: Iterable[str]) -> int:
    cubes = {tuple(map(int, line.split(','))) for line in data}
    diffs = {
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    }

    min_x, min_y, min_z = 100500, 100500, 100500
    max_x, max_y, max_z = 0, 0, 0

    for cube_x, cube_y, cube_z in cubes:
        min_x = min(cube_x, min_x)
        min_y = min(cube_y, min_y)
        min_z = min(cube_z, min_z)
        max_x = max(cube_x, max_x)
        max_y = max(cube_y, max_y)
        max_z = max(cube_z, max_z)

    min_x, min_y, min_z = min_x - 1, min_y - 1, min_z - 1
    max_x, max_y, max_z = max_x + 1, max_y + 1, max_z + 1

    queue = deque([(min_z, min_y, min_z)])
    ext_sides = set()
    visited = set()

    while queue:
        cube = queue.popleft()
        if cube in visited:
            continue
        visited.add(cube)
        cube_x, cube_y, cube_z = cube
        for diff_index, (diff_x, diff_y, diff_z) in enumerate(diffs):
            next_cube = (
                cube_x + diff_x,
                cube_y + diff_y,
                cube_z + diff_z
            )
            if not min_x <= next_cube[0] <= max_x:
                continue
            if not min_y <= next_cube[1] <= max_y:
                continue
            if not min_z <= next_cube[2] <= max_z:
                continue
            if next_cube in visited:
                continue
            if next_cube in cubes:
                ext_sides.add((next_cube, diff_index))
            else:
                queue.append(next_cube)

    return len(ext_sides)


def test_cube_ext_sides_0():
    data = [
        '1,1,1',
        '2,1,1'
    ]

    assert cube_ext_sides(data) == 10


def test_cube_ext_sides_1():
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

    assert cube_ext_sides(data) == 58


def main():
    data = sys.stdin
    result = cube_ext_sides(data)
    print(result)


if __name__ == '__main__':
    main()
