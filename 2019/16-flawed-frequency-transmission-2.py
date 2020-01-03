#!/usr/bin/env python3

import sys


def transmission(data, phases, prefix):
    offset = int(data[:7])
    repeat = 10000

    full_len = len(data) * repeat

    period_offset = (offset) % len(data)

    N = ((full_len - offset) // len(data)) + 2

    line = (data * N)[period_offset: period_offset + (full_len - offset)]

    for phase in range(phases):
        new_line = [0] * len(line)

        new_line[-1] = int(line[-1])

        for i in range(1, len(line)):
            new_line[len(line) - i - 1] = new_line[len(line) - (i - 1) - 1] + \
                int(line[len(line) - i - 1])

        line = ''.join([str(x)[-1] for x in new_line])

    return line[:8]


class TestClass:
    def test_transmission_0(self):
        data = '03036732577212944063491565474664'

        result = transmission(data, 100, 8)

        assert result == '84462026'

    def test_transmission_1(self):
        data = '02935109699940807407585447034323'

        result = transmission(data, 100, 8)

        assert result == '78725270'

    def test_transmission_2(self):
        data = '03081770884921959731165446850517'

        result = transmission(data, 100, 8)

        assert result == '53553731'


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    result = transmission(data, 100, 8)

    print(result)
