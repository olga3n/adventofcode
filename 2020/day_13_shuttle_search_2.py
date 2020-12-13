#!/usr/bin/env python3

import sys


def chinese_remainder_theorem_solution(r_list, m_list):
    M = 1

    for value in m_list:
        M *= value

    mi_list = [M // m for m in m_list]
    mi_inv_list = [pow(mi_list[i], -1, m_list[i]) for i in range(len(m_list))]

    result = 0

    for i in range(len(m_list)):
        result += r_list[i] * mi_list[i] * mi_inv_list[i]

    return result % M


def find_min_ts(data):

    bus_list = [(int(x), i) for i, x in enumerate(data.split(',')) if x != 'x']

    r_list = [bus - offset for bus, offset in bus_list]
    m_list = [bus for bus, offset in bus_list]

    result = chinese_remainder_theorem_solution(r_list, m_list)

    return result


class TestClass():

    def test_find_min_ts_1(self):
        data = [
            '7,13,x,x,59,x,31,19'
        ]

        assert find_min_ts(data[0]) == 1068781

    def test_find_min_ts_2(self):
        data = [
            '17,x,13,19'
        ]

        assert find_min_ts(data[0]) == 3417

    def test_find_min_ts_3(self):
        data = [
            '67,7,59,61'
        ]

        assert find_min_ts(data[0]) == 754018

    def test_find_min_ts_4(self):
        data = [
            '67,x,7,59,61'
        ]

        assert find_min_ts(data[0]) == 779210

    def test_find_min_ts_5(self):
        data = [
            '67,7,x,59,61'
        ]

        assert find_min_ts(data[0]) == 1261476

    def test_find_min_ts_6(self):
        data = [
            '1789,37,47,1889'
        ]

        assert find_min_ts(data[0]) == 1202161486


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = find_min_ts(data[1])
    print(result)


if __name__ == '__main__':
    main()
