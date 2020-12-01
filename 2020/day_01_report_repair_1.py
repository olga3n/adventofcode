#!/usr/bin/env python3

import sys


def find_two_items_product(data, sum_value=2020):

    diff_set = set()

    for item in data:
        if item not in diff_set:
            diff_set.add(sum_value - item)
        else:
            return item * (sum_value - item)

    return None


class TestClass():

    def test_1(self):
        data = [
            1721,
            979,
            366,
            299,
            675,
            1456
        ]

        assert find_two_items_product(data) == 514579


def main():
    data = [int(line.strip()) for line in sys.stdin if len(line.strip())]
    result = find_two_items_product(data)
    print(result)


if __name__ == '__main__':
    main()
