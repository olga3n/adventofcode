#!/usr/bin/env python3

import sys
from typing import Iterable


def tail_positions(data: Iterable[str]) -> int:
    head_pos = (0, 0)
    tail_pos = (0, 0)

    diff = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    positions = set()

    positions.add(tail_pos)

    for line in data:
        direction, value = line.split()

        for _ in range(int(value)):
            head_pos = (
                head_pos[0] + diff[direction][0],
                head_pos[1] + diff[direction][1]
            )

            tail_delta = (
                head_pos[0] - tail_pos[0],
                head_pos[1] - tail_pos[1]
            )

            if max(abs(tail_delta[0]), abs(tail_delta[1])) > 1:
                tail_pos = (
                    tail_pos[0] + tail_delta[0] // max(abs(tail_delta[0]), 1),
                    tail_pos[1] + tail_delta[1] // max(abs(tail_delta[1]), 1)
                )

                positions.add(tail_pos)

    return len(positions)


def test_tail_positions():
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

    assert tail_positions(data) == 13


def main():
    data = (line.strip() for line in sys.stdin)
    result = tail_positions(data)
    print(result)


if __name__ == '__main__':
    main()
