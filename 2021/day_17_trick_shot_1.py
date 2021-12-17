#!/usr/bin/env python3

import sys
import re


def max_y_position(data: str) -> int:
    positions = re.match(r'.+x=(.+)\.{2}(.+), y=(.+)\.{2}(.+)', data).groups()
    _, _, pos_y_min, pos_y_max = map(int, positions)

    for value in range(abs(pos_y_min), -1, -1):
        y = 0
        velocity = -value - 1

        while y > pos_y_min:
            y += y + velocity
            velocity -= 1

            if pos_y_min <= y <= pos_y_max:
                return value * (value + 1) // 2

    return 0


class TestClass():

    def test_1(self):
        data = 'target area: x=20..30, y=-10..-5'
        assert max_y_position(data) == 45


def main():
    data = next(sys.stdin).strip()
    result = max_y_position(data)
    print(result)


if __name__ == '__main__':
    main()
