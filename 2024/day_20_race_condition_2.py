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
    lines: list[str], pos: tuple[int, int], no_wall: bool = True,
) -> Iterable[tuple[int, int]]:
    for dx, dy in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
        i = pos[0] + dx
        j = pos[1] + dy

        if not 0 <= i < len(lines):
            continue

        if not 0 <= j < len(lines[i]):
            continue

        if not no_wall or lines[i][j] != '#':
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


def pos_pairs(
    lines: list[str],
) -> Iterable[tuple[tuple[int, int], tuple[int, int]]]:
    rows = len(lines)
    cols = len(lines[0])

    for i in range(rows):
        for j in range(cols):
            if lines[i][j] == '#':
                continue
            for ii in range(rows):
                for jj in range(cols):
                    if not (i, j) < (ii, jj):
                        continue
                    if lines[ii][jj] == '#':
                        continue
                    yield ((i, j), (ii, jj))


def cheats(lines: list[str], min_savings: int = 0) -> int:
    end_pos = parse_pos(lines, 'E')
    table = shortest_paths(lines, end_pos)

    stat: dict[tuple, int] = {}

    for (i, j), (ii, jj) in pos_pairs(lines):
        path_size = abs(i - ii) + abs(j - jj)

        if path_size == -1 or path_size > 20:
            continue

        diff = abs(
            table[i][j] - table[ii][jj]
        ) - path_size

        if diff > 0 and diff >= min_savings:
            if table[i][j] < table[ii][jj]:
                key = ((i, j), (ii, jj))
            else:
                key = ((ii, jj), (i, j))

            if key not in stat or stat[key] < diff:
                stat[key] = diff

    return len(stat)


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
    assert 3 == cheats(lines, min_savings=76)
    assert 285 == cheats(lines, min_savings=50)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = cheats(lines, min_savings=100)
    print(result)


if __name__ == '__main__':
    main()
