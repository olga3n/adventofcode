#!/usr/bin/env python3

import sys


def encoding_error(data, preamble=25):
    preamble_set = set(data[:preamble])

    for i in range(preamble, len(data)):
        number = data[i]
        status = False

        for ind, preamble_number in enumerate(preamble_set):
            if number - preamble_number in preamble_set:
                status = True
                break

        if not status:
            return number

        preamble_set.remove(data[i - preamble])
        preamble_set.add(number)


def find_encryption_weakness(data, preamble=25):
    data = [int(x) for x in data]
    error = encoding_error(data, preamble)

    for i in range(len(data)):
        current_sum = 0
        current_ind = i

        while current_sum < error and current_ind < len(data):
            current_sum += data[current_ind]
            current_ind += 1

        if current_sum == error:
            return min(data[i: current_ind]) + max(data[i: current_ind])


class TestClass():

    def test_find_encryption_weakness(self):
        data = [
            '35',
            '20',
            '15',
            '25',
            '47',
            '40',
            '62',
            '55',
            '65',
            '95',
            '102',
            '117',
            '150',
            '182',
            '127',
            '219',
            '299',
            '277',
            '309',
            '576'
        ]

        assert find_encryption_weakness(data, preamble=5) == 62


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = find_encryption_weakness(data, preamble=25)
    print(result)


if __name__ == '__main__':
    main()
