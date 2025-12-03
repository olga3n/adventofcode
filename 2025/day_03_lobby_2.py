#!/usr/bin/env python3

import sys
from typing import Iterable


def largest_seq(line: str, size=12) -> str:
    if size == 1:
        return max(line)

    first_symbol = max(line[:-size+1])
    seq = ''

    for i, symbol in enumerate(line):
        if symbol != first_symbol:
            continue
        if len(line) - i < size:
            break
        candidate = symbol + largest_seq(line[i+1:], size-1)
        seq = max(seq, candidate)

    return seq


def sum_largest_seq(lines: Iterable[str]) -> int:
    return sum(int(largest_seq(line.rstrip())) for line in lines)


def test_sum_largest_seq():
    lines = [
        '987654321111111',
        '811111111111119',
        '234234234234278',
        '818181911112111',
    ]
    assert 3121910778619 == sum_largest_seq(lines)


def main():
    lines = sys.stdin
    result = sum_largest_seq(lines)
    print(result)


if __name__ == '__main__':
    main()
