#!/usr/bin/env python3

import sys


def convert_code_to_number(code):
    result = 0

    for ch in code:
        result <<= 1

        if ch in ('B', 'R'):
            result += 1

    return result


def missing_seat_id(data):
    seat_id_list = []

    for code in data:
        seat_id_list.append(convert_code_to_number(code))

    missing_id = None

    seat_id_list = sorted(seat_id_list)

    for i in range(1, len(seat_id_list)):
        if seat_id_list[i] - seat_id_list[i - 1] == 2:
            missing_id = seat_id_list[i] - 1
            break

    return missing_id


class TestClass:

    def test_seat_id(self):
        assert convert_code_to_number("FBFBBFFRLR") == 357
        assert convert_code_to_number("BFFFBBFRRR") == 567
        assert convert_code_to_number("FFFBBBFRRR") == 119
        assert convert_code_to_number("BBFFBBFRLL") == 820


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = missing_seat_id(data)
    print(result)


if __name__ == '__main__':
    main()
