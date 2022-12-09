#!/usr/bin/env python3

import sys
from typing import Iterable


def tail_positions(data: Iterable[str], knots: int = 10) -> int:
    knots_pos = [(0, 0)] * knots

    diff = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    positions = set()

    positions.add(knots_pos[-1])

    for line in data:
        direction, value = line.split()

        for _ in range(int(value)):
            knots_pos[0] = (
                knots_pos[0][0] + diff[direction][0],
                knots_pos[0][1] + diff[direction][1]
            )

            for index in range(1, knots):
                curr, prev = knots_pos[index], knots_pos[index - 1]

                delta = (
                    prev[0] - curr[0],
                    prev[1] - curr[1]
                )

                if max(abs(delta[0]), abs(delta[1])) > 1:
                    knots_pos[index] = (
                        curr[0] + delta[0] // max(abs(delta[0]), 1),
                        curr[1] + delta[1] // max(abs(delta[1]), 1)
                    )

            positions.add(knots_pos[-1])

    return len(positions)


def test_tail_positions_1():
    data = [
        'R 4',
        'U 4',
        'L 3',
        'D 1',
        'R 4',
        'D 1',
        'L 5',
        'R 2'
    ]

    assert tail_positions(data) == 1


def test_tail_positions_2():
    data = [
        'R 5',
        'U 8',
        'L 8',
        'D 3',
        'R 17',
        'D 10',
        'L 25',
        'U 20'
    ]

    assert tail_positions(data) == 36


def main():
    data = (line.strip() for line in sys.stdin)
    result = tail_positions(data)
    print(result)


if __name__ == '__main__':
    main()
