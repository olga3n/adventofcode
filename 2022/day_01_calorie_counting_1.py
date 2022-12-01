#!/usr/bin/env python3

import sys
from typing import List


def max_calories(data: List[str]) -> int:
    max_result = 0
    curr_result = 0

    for line in data:
        if line:
            curr_result += int(line)
        else:
            curr_result = 0

        max_result = max(max_result, curr_result)

    return max_result


def main() -> None:
    data = [x.strip() for x in sys.stdin.readlines()]
    result = max_calories(data)
    print(result)


def test_max_calories():
    data = [
        '1000',
        '2000',
        '3000',
        '',
        '4000',
        '',
        '5000',
        '6000',
        '',
        '7000',
        '8000',
        '9000',
        '',
        '10000',
    ]

    assert max_calories(data) == 24000


if __name__ == '__main__':
    main()
