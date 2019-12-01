#!/usr/bin/env python3

import sys
import numpy as np


def calc_module_fuel(mass):
    return (np.floor(mass / 3) - 2).astype(int)


def calc_total_fuel(mass):
    return np.sum(calc_module_fuel(mass))


def parse_input(data):
    return np.array([int(x.rstrip()) for x in data])


class TestClass:
    def test_calc_module_fuel_1(self):
        mass = 12
        answer = 2

        result = calc_module_fuel(mass)

        assert result == answer

    def test_calc_module_fuel_2(self):
        mass = 14
        answer = 2

        result = calc_module_fuel(mass)

        assert result == answer

    def test_calc_module_fuel_3(self):
        mass = 1969
        answer = 654

        result = calc_module_fuel(mass)

        assert result == answer

    def test_calc_module_fuel_4(self):
        mass = 100756
        answer = 33583

        result = calc_module_fuel(mass)

        assert result == answer


if __name__ == '__main__':
    data = sys.stdin.readlines()

    mass = parse_input(data)

    result = calc_total_fuel(mass)

    print(result)
