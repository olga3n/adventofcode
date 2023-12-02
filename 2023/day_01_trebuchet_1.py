#!/usr/bin/env python3

import sys
from typing import Iterable


def calibration_value(line: str) -> int:
    first, last = -1, -1
    for symbol in line:
        if not '0' <= symbol <= '9':
            continue
        first = int(symbol) if first < 0 else first
        last = int(symbol)
    return first * 10 + last


def sum_calibration_values(data: Iterable[str]) -> int:
    return sum(calibration_value(line) for line in data)


def test_calibration_value():
    assert calibration_value('1abc2') == 12
    assert calibration_value('pqr3stu8vwx') == 38
    assert calibration_value('a1b2c3d4e5f') == 15
    assert calibration_value('treb7uchet') == 77


def test_sum_calibration_value():
    data = [
        '1abc2',
        'pqr3stu8vwx',
        'a1b2c3d4e5f',
        'treb7uchet',
    ]
    assert sum_calibration_values(data) == 142


def main():
    stdin = (line.rstrip() for line in sys.stdin)
    stdin = (line for line in stdin if len(line))
    result = sum_calibration_values(stdin)
    print(result)


if __name__ == '__main__':
    main()
