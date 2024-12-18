#!/usr/bin/env python3

import sys
from collections import deque
from typing import Iterable


def parse_coordinates(lines) -> list[tuple[int, int]]:
    coordinates = []

    for line in lines:
        values = tuple(map(int, line.split(',')))
        coordinates.append((values[0], values[1]))

    return coordinates


def gen_adj(
    table: list[list[str]], i: int, j: int,
) -> Iterable[tuple[int, int]]:
    for dx, dy in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
        ii = i + dx
        jj = j + dy

        if not 0 <= ii < len(table):
            continue

        if not 0 <= jj < len(table[0]):
            continue

        if table[ii][jj] == '.':
            yield (ii, jj)


def check_path(table: list[list[str]], size: int, max_path: int) -> bool:
    queue = deque([(0, 0, 0)])
    visited = set()

    while len(queue):
        i, j, steps = queue.popleft()

        if (i, j, steps) in visited:
            continue

        if (i, j) == (size, size):
            return True

        if steps > max_path:
            break

        visited.add((i, j, steps))

        for ii, jj in gen_adj(table, i, j):
            if not (ii, jj, steps + 1) in visited:
                queue.append((ii, jj, steps + 1))

    return False


def last_position(
    coordinates: list[tuple[int, int]], size: int, min_cnt: int,
) -> tuple[int, int]:
    left = min_cnt
    right = len(coordinates)

    while True:
        center = (left + right) // 2

        table = []

        for _ in range(size + 1):
            table.append(['.'] * (size + 1))

        for i in range(center):
            ii, jj = coordinates[i]
            table[ii][jj] = '#'

        flag = check_path(table, size, (size + 1) ** 2 - center)

        if flag:
            left = center
        else:
            right = center

        if right - left <= 1:
            return coordinates[left]

    return (-1, -1)


def test_last_position():
    lines = [
        '5,4',
        '4,2',
        '4,5',
        '3,0',
        '2,1',
        '6,3',
        '2,4',
        '1,5',
        '0,6',
        '3,3',
        '2,6',
        '5,1',
        '1,2',
        '5,5',
        '2,5',
        '6,5',
        '1,4',
        '0,4',
        '6,4',
        '1,1',
        '6,1',
        '1,0',
        '0,5',
        '1,6',
        '2,0',
    ]
    assert (6, 1) == last_position(
        parse_coordinates(lines), size=6, min_cnt=12,
    )


def main():
    lines = sys.stdin
    x, y = last_position(parse_coordinates(lines), size=70, min_cnt=1024)
    print("{},{}".format(x, y))


if __name__ == '__main__':
    main()
