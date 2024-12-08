#!/usr/bin/env python3

import sys


def antinode_locations_cnt(lines: list[str]) -> int:
    locations: dict[str, set[tuple[int, int]]] = {}

    for i in range(len(lines)):
        for j, symbol in enumerate(lines[i]):
            if symbol != '.':
                if symbol not in locations:
                    locations[symbol] = {(i, j)}
                else:
                    locations[symbol].add((i, j))

    pos_set: set[tuple[int, int]] = set()

    for symbol, positions in locations.items():
        pairs = (
            (x, y)
            for x in positions
            for y in positions
            if x < y
        )

        for pos_1, pos_2 in pairs:
            dx = pos_1[0] - pos_2[0]
            dy = pos_1[1] - pos_2[1]

            for i in range(max(len(lines), len(lines[0]))):
                x0 = pos_2[0] - i * dx
                y0 = pos_2[1] - i * dy

                if 0 <= x0 < len(lines) and 0 <= y0 < len(lines[0]):
                    pos_set.add((x0, y0))
                else:
                    break

            for i in range(max(len(lines), len(lines[0]))):
                x1 = pos_1[0] + i * dx
                y1 = pos_1[1] + i * dy

                if 0 <= x1 < len(lines) and 0 <= y1 < len(lines[0]):
                    pos_set.add((x1, y1))
                else:
                    break

    return len(pos_set)


def test_antinode_locations_cnt():
    lines = [
        '............',
        '........0...',
        '.....0......',
        '.......0....',
        '....0.......',
        '......A.....',
        '............',
        '............',
        '........A...',
        '.........A..',
        '............',
        '............',
    ]
    assert 34 == antinode_locations_cnt(lines)


def main():
    lines = list(line.rstrip() for line in sys.stdin)
    result = antinode_locations_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()
