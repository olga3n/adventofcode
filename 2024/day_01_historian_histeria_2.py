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


def frequency(values: list[int]) -> dict[int, int]:
    freq: dict[int, int] = {}
    for value in values:
        freq[value] = freq.get(value, 0) + 1
    return freq


def similarity_score(list_1: list[int], list_2: list[int]) -> int:
    freq = frequency(list_2)
    return sum(value * freq.get(value, 0) for value in list_1)


def test_similarity_score():
    lines = [
        '3   4',
        '4   3',
        '2   5',
        '1   3',
        '3   9',
        '3   3',
    ]
    assert 31 == similarity_score(*parse_lines(lines))


def main():
    lines = sys.stdin
    result = similarity_score(*parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
