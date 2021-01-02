#!/usr/bin/env python3

import sys


def encryption_key(data):
    key_1, key_2 = int(data[0]), int(data[1])
    loop_size_1, loop_size_2 = None, None

    loop_size = 1
    subject_number = 7
    value = 1

    while True:
        value = (value * subject_number) % 20201227

        if value == key_1:
            loop_size_1 = loop_size

        if value == key_2:
            loop_size_2 = loop_size

        if loop_size_1 or loop_size_2:
            break

        loop_size += 1

    key = key_2 if loop_size_1 else key_1
    loop_size = loop_size_1 if loop_size_1 else loop_size_2

    subject_number = key
    value = 1

    for i in range(loop_size):
        value = (value * subject_number) % 20201227

    return value


class TestClass():

    def test_encryption_key(self):
        data = [
            '5764801',
            '17807724'
        ]

        assert encryption_key(data) == 14897079


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = encryption_key(data)
    print(result)


if __name__ == '__main__':
    main()
