#!/usr/bin/env python3

import sys


def transmission(data, phases, prefix):

    pattern = [0, 1, 0, -1]

    line = data

    for phase in range(phases):
        new_line = [0] * len(line)

        for i in range(len(line)):
            for j, ch in enumerate(line):
                ind = (((j + 1) % (len(pattern) * (i + 1))) // (i + 1))
                new_line[i] += int(ch) * pattern[ind]

        line = ''.join([str(x)[-1] for x in new_line])

    return line[:8]


class TestClass:
    def test_transmission_0(self):
        data = '12345678'

        result = transmission(data, 4, 8)

        assert result == '01029498'

    def test_transmission_1(self):
        data = '80871224585914546619083218645595'

        result = transmission(data, 100, 8)

        assert result == '24176176'

    def test_transmission_2(self):
        data = '19617804207202209144916044189917'

        result = transmission(data, 100, 8)

        assert result == '73745418'

    def test_transmission_3(self):
        data = '69317163492948606335995924319873'

        result = transmission(data, 100, 8)

        assert result == '52432133'


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    result = transmission(data, 100, 8)

    print(result)
