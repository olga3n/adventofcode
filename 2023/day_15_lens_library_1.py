#!/usr/bin/env python3

import sys
from typing import List


def seq_score(seq: str) -> int:
    current_value = 0

    for char in seq:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def sum_score(data: List[str]) -> int:
    return sum(seq_score(seq) for seq in data)


def test_seq_score():
    assert seq_score('HASH') == 52


def test_sum_score():
    data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    assert sum_score(data.split(',')) == 1320


def main():
    data = sys.stdin.read().rstrip('\n')
    result = sum_score(data.split(','))
    print(result)


if __name__ == '__main__':
    main()
