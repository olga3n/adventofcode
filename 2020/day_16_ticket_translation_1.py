#!/usr/bin/env python3

import sys


def check_value(limits, value):
    result = False

    for name, limits_ranges in limits.items():
        for value_min, value_max in limits_ranges:
            if value_min <= value <= value_max:
                result = True
                break

    return result


def scan_error_rate(data):

    limits = {}

    for i, line in enumerate(data):
        if not len(line):
            continue

        if line == 'your ticket:':
            break

        name, limits_line = line.split(': ')

        limits_ranges = limits_line.split(' or ')
        limits_ranges = [
            tuple(map(int, x.split('-'))) for x in limits_ranges
        ]

        limits[name] = limits_ranges

    result = 0
    status = False

    for line in data:
        if line == 'nearby tickets:':
            status = True
            continue

        if status:
            values = list(map(int, line.split(',')))

            for value in values:
                if not check_value(limits, value):
                    result += value

    return result


class TestClass():

    def test_scan_error_rate(self):
        data = [
            'class: 1-3 or 5-7',
            'row: 6-11 or 33-44',
            'seat: 13-40 or 45-50',
            '',
            'your ticket:',
            '7,1,14',
            '',
            'nearby tickets:',
            '7,3,47',
            '40,4,50',
            '55,2,20',
            '38,6,12'
        ]

        assert scan_error_rate(data) == 71


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = scan_error_rate(data)
    print(result)


if __name__ == '__main__':
    main()
