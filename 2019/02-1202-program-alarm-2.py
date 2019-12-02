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


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    orig_registers = parse_input(data)

    for noun in range(0, 100):
        for verb in range(0, 100):
            registers = np.copy(orig_registers)

            registers[1] = noun
            registers[2] = verb

            registers = run_program(registers)

            if registers[0] == 19690720:
                result = noun * 100 + verb
                break

        if registers[0] == 19690720:
            break

    print(result)
