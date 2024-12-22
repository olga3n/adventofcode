#!/usr/bin/env python3

import sys
from collections import deque
from typing import Iterable


def parse_pos(lines: list[str], symbol: str) -> tuple[int, int]:
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == symbol:
                return (i, j)
    return (-1, -1)


def gen_next(
    lines: list[str], pos: tuple[int, int],
) -> Iterable[tuple[int, int]]:
    for dx, dy in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
        i = pos[0] + dx
        j = pos[1] + dy

        if not 0 <= i < len(lines):
            continue

        if not 0 <= j < len(lines[i]):
            continue

        if lines[i][j] != '#':
            yield (i, j)


def shortest_paths(
    lines: list[str], start_pos: tuple[int, int],
) -> list[list[int]]:
    queue = deque([(start_pos, 0)])
    table = []

    for i in range(len(lines)):
        table.append([-1] * len(lines[i]))

    while len(queue):
        pos, size = queue.popleft()

        if table[pos[0]][pos[1]] == -1:
            table[pos[0]][pos[1]] = size
        else:
            continue

        for i, j in gen_next(lines, pos):
            queue.append(((i, j), size + 1))

    return table


def cheats(lines: list[str], min_savings: int = 0) -> int:
    end_pos = parse_pos(lines, 'E')
    table = shortest_paths(lines, end_pos)
    result = 0

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != '#':
                continue

            adj = list(gen_next(lines, (i, j)))
            for ii in range(len(adj)):
                for jj in range(ii, len(adj)):
                    one = adj[ii]
                    two = adj[jj]
                    diff = abs(
                        table[one[0]][one[1]] - table[two[0]][two[1]]
                    ) - 2

                    if diff > 0 and diff >= min_savings:
                        result += 1

    return result


def test_cheats():
    lines = [
        '###############',
        '#...#...#.....#',
        '#.#.#.#.#.###.#',
        '#S#...#.#.#...#',
        '#######.#.#.###',
        '#######.#.#...#',
        '#######.#.###.#',
        '###..E#...#...#',
        '###.#######.###',
        '#...###...#...#',
        '#.#####.#.###.#',
        '#.#...#.#.#...#',
        '#.#.#.#.#.#.###',
        '#...#...#...###',
        '###############',
    ]
    assert 1 == cheats(lines, min_savings=64)
    assert 44 == cheats(lines, min_savings=0)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = cheats(lines, min_savings=100)
    print(result)


if __name__ == '__main__':
    main()
