#!/usr/bin/env python3

import sys


def valid_passwords(data):
    result = 0

    for line in data:
        tokens = line.split(' ')

        min_count, max_count = list(map(int, tokens[0].split('-')))
        char = tokens[1][:-1]

        count = sum([1 for x in tokens[2] if x == char])

        if min_count <= count <= max_count:
            result += 1

    return result


class TestClass:

    def test_1(self):
        data = [
            '1-3 a: abcde',
            '1-3 b: cdefg',
            '2-9 c: ccccccccc'
        ]

        assert valid_passwords(data) == 2


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = valid_passwords(data)
    print(result)


if __name__ == '__main__':
    main()
