#!/usr/bin/env python3

import sys


def find_three_items_product(data, sum_value=2020):

    diff_dict = {}

    for i, item_1 in enumerate(data):
        for j, item_2 in enumerate(data):
            if i < j:
                diff_dict[sum_value - (item_1 + item_2)] = (i, j)

        if item_1 in diff_dict and i not in diff_dict[item_1]:
            ind_1, ind_2 = diff_dict[item_1]
            return item_1 * data[ind_1] * data[ind_2]

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

        assert find_three_items_product(data) == 241861950


def main():
    data = [int(line.strip()) for line in sys.stdin if len(line.strip())]
    result = find_three_items_product(data)
    print(result)


if __name__ == '__main__':
    main()
