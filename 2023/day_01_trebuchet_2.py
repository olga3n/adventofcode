#!/usr/bin/env python3

import sys
from typing import Iterable

DIGIT_VALUE = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


def calibration_value(line: str) -> int:
    first, last = -1, -1

    for index, symbol in enumerate(line):
        if '0' <= symbol <= '9':
            digit = int(symbol)
        else:
            digit = -1
            for name in DIGIT_VALUE:
                if line[index: index + len(name)] == name:
                    digit = DIGIT_VALUE[name]
                    break
        if digit > 0:
            first = digit if first < 0 else first
            last = digit

    return first * 10 + last


def sum_calibration_values(data: Iterable[str]) -> int:
    return sum(calibration_value(line) for line in data)


def test_calibration_value():
    assert calibration_value('two1nine') == 29
    assert calibration_value('eightwothree') == 83
    assert calibration_value('abcone2threexyz') == 13
    assert calibration_value('xtwone3four') == 24
    assert calibration_value('4nineeightseven2') == 42
    assert calibration_value('zoneight234') == 14
    assert calibration_value('7pqrstsixteen') == 76


def test_sum_calibration_value():
    data = [
        'two1nine',
        'eightwothree',
        'abcone2threexyz',
        'xtwone3four',
        '4nineeightseven2',
        'zoneight234',
        '7pqrstsixteen',
    ]
    assert sum_calibration_values(data) == 281


def main():
    stdin = (line.rstrip() for line in sys.stdin)
    stdin = (line for line in sys.stdin if len(line))
    result = sum_calibration_values(stdin)
    print(result)


if __name__ == '__main__':
    main()
