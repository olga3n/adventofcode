#!/usr/bin/env python3

import sys
from typing import Iterable


def increases_count(data: Iterable[int]) -> int:
    result = 0
    prev_value = 0

    for index, value in enumerate(data):
        if index != 0:
            if value > prev_value:
                result += 1
        prev_value = value

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

        assert increases_count(data) == 7


def main():
    data = map(int, sys.stdin)
    result = increases_count(data)
    print(result)


if __name__ == '__main__':
    main()
