#!/usr/bin/env python3

import sys


def find_next_number(data, count=30000000):

    numbers = list(map(int, data.split(',')))
    hist = {value: i for i, value in enumerate(numbers)}

    value = numbers[-1]
    next_value = 0

    for i in range(len(numbers), count):
        value = next_value

        if value not in hist:
            next_value = 0
        else:
            next_value = i - hist[value]

        hist[value] = i

    return value


class TestClass():

    def test_find_next_number(self):
        assert find_next_number('0,3,6') == 175594
        assert find_next_number('1,3,2') == 2578
        assert find_next_number('2,1,3') == 3544142
        assert find_next_number('1,2,3') == 261214
        assert find_next_number('2,3,1') == 6895259
        assert find_next_number('3,2,1') == 18
        assert find_next_number('3,1,2') == 362


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = find_next_number(data[0])
    print(result)


if __name__ == '__main__':
    main()
