#!/usr/bin/env python3

import sys
from typing import Iterable


def gen_adj(lines: list[str], i: int, j: int) -> Iterable[tuple[int, int]]:
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ii = i + dx
        jj = j + dy

        if not 0 <= ii < len(lines):
            continue

        if not 0 <= jj < len(lines[0]):
            continue

        if lines[i][j] != lines[ii][jj]:
            continue

        yield (ii, jj)


def area_score(
    lines: list[str], visited: list[list[bool]], i: int, j: int,
) -> int:

    stack = [(i, j)]
    perimiter = 0
    area = 0

    while stack:
        i, j = stack.pop()

        if visited[i][j]:
            continue

        visited[i][j] = True
        perimiter += 4
        area += 1

        for ii, jj in gen_adj(lines, i, j):
            stack.append((ii, jj))
            perimiter -= 1

    return area * perimiter


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
    assert 140 == total_price(lines)


def test_total_price_1():
    lines = [
        'OOOOO',
        'OXOXO',
        'OOOOO',
        'OXOXO',
        'OOOOO',
    ]
    assert 772 == total_price(lines)


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
    assert 1930 == total_price(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = total_price(lines)
    print(result)


if __name__ == '__main__':
    main()
