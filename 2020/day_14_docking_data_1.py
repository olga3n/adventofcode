#!/usr/bin/env python3

import sys


def memory_sum(data):

    memory = {}
    max_value = (1 << 36) - 1

    for line in data:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]

            mask_0 = int(''.join(['1' if x == '0' else '0' for x in mask]), 2)
            mask_1 = int(''.join(['1' if x == '1' else '0' for x in mask]), 2)

        elif line.startswith('mem'):
            addr, value = line.split(' = ')

            addr = int(addr[4: -1])
            value = int(value)

            value = value & (max_value - mask_0)
            value = (value & (max_value - mask_1)) + mask_1

            memory[addr] = value

    return sum(memory.values())


class TestClass():

    def test_memory_sum(self):
        data = [
            'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
            'mem[8] = 11',
            'mem[7] = 101',
            'mem[8] = 0'
        ]

        assert memory_sum(data) == 165


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = memory_sum(data)
    print(result)


if __name__ == '__main__':
    main()
