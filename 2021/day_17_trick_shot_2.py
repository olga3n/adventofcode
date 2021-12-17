#!/usr/bin/env python3

import sys
import re


def distinct_values(data: str) -> int:
    positions = re.match(r'.+x=(.+)\.{2}(.+), y=(.+)\.{2}(.+)', data).groups()
    pos_x_min, pos_x_max, pos_y_min, pos_y_max = map(int, positions)
    result = 0

    for y_value in range(pos_y_min, abs(pos_y_min) + 1):
        for x_value in range(pos_x_max + 1):
            x, y = 0, 0
            x_velocity, y_velocity = x_value, y_value

            while x < pos_x_max and y > pos_y_min:
                x += x_velocity
                y += y_velocity

                if x_velocity < 0:
                    x_velocity += 1
                elif x_velocity > 0:
                    x_velocity -= 1

                y_velocity -= 1

                if pos_y_min <= y <= pos_y_max and pos_x_min <= x <= pos_x_max:
                    result += 1
                    break

    return result


class TestClass():

    def test_1(self):
        data = 'target area: x=20..30, y=-10..-5'
        assert distinct_values(data) == 112


def main():
    data = next(sys.stdin).strip()
    result = distinct_values(data)
    print(result)


if __name__ == '__main__':
    main()
