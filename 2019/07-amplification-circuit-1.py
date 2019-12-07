#!/usr/bin/env python3

import sys
import itertools
import numpy as np


def run_program(registers, inputs):
    ip = 0

    outputs = []
    current_input_index = 0

    while True:
        instruction = '0' * 4 + str(registers[ip])

        opcode = int(instruction[-2:])

        ax_mode = int(instruction[-3])
        bx_mode = int(instruction[-4])
        cx_mode = int(instruction[-5])

        if 1 <= opcode <= 2:
            ax = registers[ip + 1]
            bx = registers[ip + 2]
            cx = registers[ip + 3]

            arg1 = registers[ax] if ax_mode == 0 else ax
            arg2 = registers[bx] if bx_mode == 0 else bx

            if opcode == 1:
                registers[cx] = arg1 + arg2
            elif opcode == 2:
                registers[cx] = arg1 * arg2

            ip += 4

        elif 3 <= opcode <= 4:
            ax = registers[ip + 1]

            if opcode == 3:
                registers[ax] = inputs[current_input_index]
                current_input_index += 1

            elif opcode == 4:
                arg1 = registers[ax] if ax_mode == 0 else ax
                outputs.append(arg1)

            ip += 2
        elif 5 <= opcode <= 6:
            ax = registers[ip + 1]
            bx = registers[ip + 2]

            arg1 = registers[ax] if ax_mode == 0 else ax
            arg2 = registers[bx] if bx_mode == 0 else bx

            if opcode == 5:
                ip = arg2 if arg1 != 0 else ip + 3
            elif opcode == 6:
                ip = arg2 if arg1 == 0 else ip + 3

        elif 7 <= opcode <= 8:
            ax = registers[ip + 1]
            bx = registers[ip + 2]
            cx = registers[ip + 3]

            arg1 = registers[ax] if ax_mode == 0 else ax
            arg2 = registers[bx] if bx_mode == 0 else bx

            if opcode == 7:
                registers[cx] = 1 if arg1 < arg2 else 0
            elif opcode == 8:
                registers[cx] = 1 if arg1 == arg2 else 0

            ip += 4

        elif opcode == 99:
            break

    return outputs


def max_signal(registers):
    max_signal = 0
    best_settings = [0, 1, 2, 3, 4]

    for settings in itertools.permutations([0, 1, 2, 3, 4]):
        signal = 0

        for i in range(0, 5):
            output = run_program(
                np.copy(registers), [settings[i], signal])[0]

            signal = output

        if signal > max_signal:
            max_signal = signal
            best_settings = list(settings)

    return max_signal, best_settings


def parse_input(data):
    return np.array([int(x) for x in data.split(',') if x])


class TestClass:
    def test_max_signal_1(self):
        registers = parse_input(
            '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')

        result, settings = max_signal(registers)

        assert (result == 43210) and (settings == [4, 3, 2, 1, 0])

    def test_max_signal_2(self):
        registers = parse_input(
            '3,23,3,24,1002,24,10,24,1002,23,-1,23,'
            '101,5,23,23,1,24,23,23,4,23,99,0,0')

        result, settings = max_signal(registers)

        assert (result == 54321) and (settings == [0, 1, 2, 3, 4])

    def test_max_signal_3(self):
        registers = parse_input(
            '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,'
            '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')

        result, settings = max_signal(registers)

        assert (result == 65210) and (settings == [1, 0, 4, 3, 2])


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    result, _ = max_signal(registers)

    print(result)
