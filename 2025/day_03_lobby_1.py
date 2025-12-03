#!/usr/bin/env python3

import sys
from typing import Iterable


def largest_seq(line: str) -> str:
    seq = ''
    curr_max = line[0]

    for i in range(1, len(line)):
        candidate = curr_max + line[i]
        seq = max(seq, candidate)
        curr_max = max(curr_max, line[i])

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
    assert 357 == sum_largest_seq(lines)


def main():
    lines = sys.stdin
    result = sum_largest_seq(lines)
    print(result)


if __name__ == '__main__':
    main()
