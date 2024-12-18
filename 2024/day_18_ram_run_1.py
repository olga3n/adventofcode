#!/usr/bin/env python3

import sys
from collections import deque
from typing import Iterable


def parse_coordinates(lines, cnt: int) -> Iterable[tuple[int, int]]:
    i = 0

    for line in lines:
        values = tuple(map(int, line.split(',')))
        yield (values[0], values[1])
        i += 1
        if i == cnt:
            return


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


def min_path_len(coordinates: Iterable[tuple[int, int]], size: int) -> int:
    table = []

    for _ in range(size + 1):
        table.append(['.'] * (size + 1))

    queue = deque([(0, 0, 0)])
    visited = set()

    for ii, jj in coordinates:
        table[ii][jj] = '#'

    result = 0

    while len(queue):
        i, j, steps = queue.popleft()

        if (i, j, steps) in visited:
            continue

        if (i, j) == (size, size):
            result = steps
            break

        visited.add((i, j, steps))

        for ii, jj in gen_adj(table, i, j):
            queue.append((ii, jj, steps + 1))

    return result


def test_min_path_len():
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
    assert 22 == min_path_len(parse_coordinates(lines, cnt=12), size=6)


def main():
    lines = sys.stdin
    result = min_path_len(parse_coordinates(lines, cnt=1024), size=70)
    print(result)


if __name__ == '__main__':
    main()
