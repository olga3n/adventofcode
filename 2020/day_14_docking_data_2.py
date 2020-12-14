#!/usr/bin/env python3

import sys


def memory_sum(data):

    memory = {}
    max_value = (1 << 36) - 1

    for line in data:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]

            mask_1 = int(''.join(['1' if x == '1' else '0' for x in mask]), 2)

            mask_x = [
                1 << (len(mask) - i - 1)
                for i, x in enumerate(mask) if x == 'X'
            ]

        elif line.startswith('mem'):
            addr, value = line.split(' = ')

            addr = int(addr[4: -1])
            value = int(value)

            addr = (addr & (max_value - mask_1)) + mask_1

            for number in range(1 << len(mask_x)):
                new_addr = addr

                for i, m in enumerate(mask_x):
                    coeff = 1 if number & (1 << i) > 0 else 0
                    new_addr = (new_addr & (max_value - m)) + coeff * m

                memory[new_addr] = value

    return sum(memory.values())


class TestClass():

    def test_memory_sum(self):
        data = [
            'mask = 000000000000000000000000000000X1001X',
            'mem[42] = 100',
            'mask = 00000000000000000000000000000000X0XX',
            'mem[26] = 1'
        ]

        assert memory_sum(data) == 208


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = memory_sum(data)
    print(result)


if __name__ == '__main__':
    main()
