#!/usr/bin/env python3

import sys
from typing import Tuple


def reachable_tiles(data: Tuple[str], steps: int, start='S') -> int:
    for i, line in enumerate(data):
        j = line.find(start)
        if j >= 0:
            start_pos = (i, j)
            break

    tiles = {start_pos}

    for _ in range(steps):
        new_tiles = set()

        for pos in tiles:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                xx, yy = pos[0] + dx, pos[1] + dy
                if not 0 <= xx < len(data):
                    continue
                if not 0 <= yy < len(data[0]):
                    continue
                if data[xx][yy] == '#':
                    continue
                new_tiles.add((xx, yy))

        tiles = new_tiles

    for i, line in enumerate(data):
        for j in range(len(line)):
            if (i, j) in tiles:
                print('O', end='', file=sys.stderr)
            else:
                print(data[i][j], end='', file=sys.stderr)
        print(file=sys.stderr)

    return len(tiles)


def test_tiles_count():
    data = [
        '...........',
        '.....###.#.',
        '.###.##..#.',
        '..#.#...#..',
        '....#.#....',
        '.##..S####.',
        '.##..#...#.',
        '.......##..',
        '.##.#.####.',
        '.##..##.##.',
        '...........',
    ]
    assert reachable_tiles(data, steps=6) == 16


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = tuple(line for line in data if len(line))
    result = reachable_tiles(data, steps=64)
    print(result)


if __name__ == '__main__':
    main()
