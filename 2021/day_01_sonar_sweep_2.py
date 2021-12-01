#!/usr/bin/env python3

import sys
from typing import Iterable


def increases_count(data: Iterable[int]) -> int:
    result = 0
    prev_sum = 0

    value_1, value_2 = 0, 0

    for index, value in enumerate(data):
        if index > 2:
            next_sum = value_1 + value_2 + value

            if next_sum > prev_sum:
                result += 1

            prev_sum = next_sum

        value_1, value_2 = value_2, value

    return result


class TestClass():

    def test_1(self):
        data = [
            199,
            200,
            208,
            210,
            200,
            207,
            240,
            269,
            260,
            263
        ]

        assert increases_count(data) == 5


def main():
    data = map(int, sys.stdin)
    result = increases_count(data)
    print(result)


if __name__ == '__main__':
    main()
