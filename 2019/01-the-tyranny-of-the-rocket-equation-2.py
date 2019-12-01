#!/usr/bin/env python3

import sys
import numpy as np


def calc_module_fuel(mass):
    return (np.floor(mass / 3) - 2).astype(int)


def calc_full_module_fuel(mass):
    result = 0
    current_mass = mass

    while True:
        current_fuel = calc_module_fuel(current_mass)

        if current_fuel <= 0:
            break

        result += current_fuel
        current_mass = current_fuel

    return result


def calc_total_fuel(mass):
    return np.sum([calc_full_module_fuel(x) for x in mass])


def parse_input(data):
    return [int(x.rstrip()) for x in data]


class TestClass:
    def test_calc_full_module_fuel_1(self):
        mass = 12
        answer = 2

        result = calc_full_module_fuel(mass)

        assert result == answer

    def test_calc_full_module_fuel_2(self):
        mass = 1969
        answer = 966

        result = calc_full_module_fuel(mass)

        assert result == answer

    def test_calc_full_module_fuel_3(self):
        mass = 100756
        answer = 50346

        result = calc_full_module_fuel(mass)

        assert result == answer


if __name__ == '__main__':
    data = sys.stdin.readlines()

    mass = parse_input(data)

    result = calc_total_fuel(mass)

    print(result)
