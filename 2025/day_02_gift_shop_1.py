#!/usr/bin/env python3

import sys
from typing import Iterable, Tuple


def parse_ranges(line) -> Iterable[Tuple[int, int]]:
    for rng_text in line.split(','):
        left, right = rng_text.split('-')
        yield int(left), int(right)


def is_invalid(value: int) -> bool:
    str_value = str(value)
    if len(str_value) > 1 and len(str_value) % 2 == 0:
        center = len(str_value) // 2
        if str_value[:center] == str_value[center:]:
            return True
    return False


def invalid_ids(line: str) -> int:
    result = 0

    for left, right in parse_ranges(line):
        for value in range(left, right + 1):
            if is_invalid(value):
                result += value

    return result


def test_zero_turns():
    line = (
        '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,'
        '1698522-1698528,446443-446449,38593856-38593862,565653-565659,'
        '824824821-824824827,2121212118-2121212124'
    )
    assert 1227775554 == invalid_ids(line)


def main():
    line = sys.stdin.readline()
    result = invalid_ids(line)
    print(result)


if __name__ == '__main__':
    main()
