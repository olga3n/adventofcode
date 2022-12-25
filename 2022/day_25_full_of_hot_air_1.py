#!/usr/bin/env python3

import sys
import math
from typing import Iterable


def parse_number(line: str) -> int:
    result = 0

    for index, symbol in enumerate(line[::-1]):
        if symbol == '-':
            value = -1
        elif symbol == '=':
            value = -2
        else:
            value = int(symbol)
        result += (5 ** index) * value

    return result


def number_to_snafu(number: int) -> str:
    digits = {}

    while number:
        max_degree = int(math.log(number, 5))
        coeff = number // (5 ** max_degree)
        number -= coeff * (5 ** max_degree)
        digits[max_degree] = coeff

    result = ''

    for degree in range(max(digits) + 3):
        value = digits.get(degree, 0)
        if 0 <= value <= 2:
            result = str(value) + result
        elif value == 3:
            result = '=' + result
            if degree + 1 not in digits:
                digits[degree + 1] = 1
            else:
                digits[degree + 1] += 1
        elif value == 4:
            result = '-' + result
            if degree + 1 not in digits:
                digits[degree + 1] = 1
            else:
                digits[degree + 1] += 1
        elif value >= 5:
            if degree + 1 not in digits:
                digits[degree + 1] = 1
            else:
                digits[degree + 1] += 1
            result = str(value - 5) + result

    return result.lstrip('0')


def sum_snafu(data: Iterable[str]) -> str:
    sum_number = sum(parse_number(line.rstrip()) for line in data)
    return number_to_snafu(sum_number)


def test_number_to_snafu():
    assert number_to_snafu(1) == '1'
    assert number_to_snafu(2) == '2'
    assert number_to_snafu(3) == '1='
    assert number_to_snafu(4) == '1-'
    assert number_to_snafu(5) == '10'
    assert number_to_snafu(6) == '11'
    assert number_to_snafu(7) == '12'
    assert number_to_snafu(8) == '2='
    assert number_to_snafu(9) == '2-'
    assert number_to_snafu(10) == '20'
    assert number_to_snafu(15) == '1=0'
    assert number_to_snafu(20) == '1-0'
    assert number_to_snafu(2022) == '1=11-2'
    assert number_to_snafu(12345) == '1-0---0'
    assert number_to_snafu(314159265) == '1121-1110-1=0'


def test_sum_snafu():
    data = [
        '1=-0-2',
        '12111',
        '2=0=',
        '21',
        '2=01',
        '111',
        '20012',
        '112',
        '1=-1=',
        '1-12',
        '12',
        '1=',
        '122'
    ]

    assert sum_snafu(data) == "2=-1=0"


def main():
    data = sys.stdin
    result = sum_snafu(data)
    print(result)


if __name__ == '__main__':
    main()
