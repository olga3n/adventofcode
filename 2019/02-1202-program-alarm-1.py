#!/usr/bin/env python3

import sys
import numpy as np


def run_program(registers):
    ip = 0

    while True:
        opcode = registers[ip]

        if opcode == 99:
            break

        ax = registers[ip + 1]
        bx = registers[ip + 2]
        cx = registers[ip + 3]

        if opcode == 1:
            registers[cx] = registers[ax] + registers[bx]

        if opcode == 2:
            registers[cx] = registers[ax] * registers[bx]

        ip += 4

    return registers


def parse_input(line):
    registers = np.array([int(x) for x in line.split(',')])
    return registers


class TestClass:
    def test_run_program_1(self):
        registers = parse_input('1,9,10,3,2,3,11,0,99,30,40,50')
        registers = run_program(registers)
        assert registers[0] == 3500

    def test_run_program_2(self):
        registers = parse_input('1,0,0,0,99')
        registers = run_program(registers)
        assert np.array_equal(
            registers,
            np.array([2, 0, 0, 0, 99]))

    def test_run_program_3(self):
        registers = parse_input('2,3,0,3,99')
        registers = run_program(registers)
        assert np.array_equal(
            registers,
            np.array([2, 3, 0, 6, 99]))

    def test_run_program_4(self):
        registers = parse_input('2,4,4,5,99,0')
        registers = run_program(registers)
        assert np.array_equal(
            registers,
            np.array([2, 4, 4, 5, 99, 9801]))

    def test_run_program_4(self):
        registers = parse_input('1,1,1,4,99,5,6,0,99')
        registers = run_program(registers)
        assert np.array_equal(
            registers,
            np.array([30, 1, 1, 4, 2, 5, 6, 0, 99]))


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    registers = parse_input(data)

    registers[1] = 12
    registers[2] = 2

    registers = run_program(registers)

    result = registers[0]

    print(result)
