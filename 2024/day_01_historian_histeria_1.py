#!/usr/bin/env python3

import sys
from typing import Iterable


def parse_lines(lines: Iterable[str]) -> tuple[list[int], list[int]]:
    list_1, list_2 = [], []

    for line in lines:
        number_1, number_2 = map(int, line.split())
        list_1.append(number_1)
        list_2.append(number_2)

    return (list_1, list_2)


def distance(left: int, right: int) -> int:
    value = left - right
    return value if value > 0 else -value


def total_distance(list_1: list[int], list_2: list[int]) -> int:
    list_1.sort()
    list_2.sort()
    return sum(distance(list_1[i], list_2[i]) for i in range(len(list_1)))


def test_total_distance():
    lines = [
        '3   4',
        '4   3',
        '2   5',
        '1   3',
        '3   9',
        '3   3',
    ]
    assert 11 == total_distance(*parse_lines(lines))


def main():
    lines = sys.stdin
    result = total_distance(*parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
