#!/usr/bin/env python3

import sys


def find_next_bus(data):

    first_ts = int(data[0])
    bus_list = [int(x) for x in data[1].split(',') if x != 'x']

    result = 0
    ts = first_ts

    while True:
        for bus in bus_list:
            if ts % bus == 0:
                result = (ts - first_ts) * bus
                break

        if result != 0:
            break

        ts += 1

    return result


class TestClass():

    def test_find_next_bus(self):
        data = [
            '939',
            '7,13,x,x,59,x,31,19'
        ]

        assert find_next_bus(data) == 295


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = find_next_bus(data)
    print(result)


if __name__ == '__main__':
    main()
