#!/usr/bin/env python3

import sys
from typing import Iterable


def sequence_score(line: str) -> int:
    values = list(map(int, line.split()))
    coeff = 0

    while not all(value == 0 for value in values):
        coeff += values[-1]
        values = [values[i + 1] - values[i] for i in range(len(values) - 1)]

    return coeff


def total_score(data: Iterable[str]) -> int:
    return sum(sequence_score(line) for line in data)


def test_sequence_score():
    data = [
        '0 3 6 9 12 15',
        '1 3 6 10 15 21',
        '10 13 16 21 30 45',
    ]
    assert sequence_score(data[0]) == 18
    assert sequence_score(data[1]) == 28
    assert sequence_score(data[2]) == 68


def test_total_score():
    data = [
        '0 3 6 9 12 15',
        '1 3 6 10 15 21',
        '10 13 16 21 30 45',
    ]
    assert total_score(data) == 114


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = total_score(data)
    print(result)


if __name__ == '__main__':
    main()
