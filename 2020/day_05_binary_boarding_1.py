#!/usr/bin/env python3

import sys


def convert_code_to_number(code):
    result = 0

    for ch in code:
        result <<= 1

        if ch in ('B', 'R'):
            result += 1

    return result


def max_seat_id(data):
    max_id = 0

    for code in data:
        max_id = max(max_id, convert_code_to_number(code))

    return max_id


class TestClass:

    def test_seat_id(self):
        assert convert_code_to_number("FBFBBFFRLR") == 357
        assert convert_code_to_number("BFFFBBFRRR") == 567
        assert convert_code_to_number("FFFBBBFRRR") == 119
        assert convert_code_to_number("BBFFBBFRLL") == 820

    def test_max_seat_id(self):
        data = [
            'BFFFBBFRRR',
            'FFFBBBFRRR',
            'BBFFBBFRLL'
        ]

        assert max_seat_id(data) == 820


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = max_seat_id(data)
    print(result)


if __name__ == '__main__':
    main()
