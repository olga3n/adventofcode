#!/usr/bin/env python3

import sys


def valid_passwords(data):
    result = 0

    for line in data:
        tokens = line.split(' ')

        ind_1, ind_2 = list(map(int, tokens[0].split('-')))
        char = tokens[1][:-1]
        password = tokens[2]

        if password[ind_1 - 1] != password[ind_2 - 1]:
            if char in (password[ind_1 - 1], password[ind_2 - 1]):
                result += 1

    return result


class TestClass:

    def test_1(self):
        data = [
            '1-3 a: abcde',
            '1-3 b: cdefg',
            '2-9 c: ccccccccc'
        ]

        assert valid_passwords(data) == 1


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = valid_passwords(data)
    print(result)


if __name__ == '__main__':
    main()
