#!/usr/bin/env python3

import sys
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

            if opcode == 1:
                registers[cx] = \
                    (registers[ax] if ax_mode == 0 else ax) + \
                    (registers[bx] if bx_mode == 0 else bx)
            elif opcode == 2:
                registers[cx] = \
                    (registers[ax] if ax_mode == 0 else ax) * \
                    (registers[bx] if bx_mode == 0 else bx)

            ip += 4

        elif opcode == 3:
            ax = registers[ip + 1]

            registers[ax] = inputs[current_input_index]
            current_input_index += 1

            ip += 2
        elif opcode == 4:
            ax = registers[ip + 1]

            outputs.append((registers[ax] if ax_mode == 0 else ax))

            ip += 2
        elif opcode == 99:
            break

    return outputs


def parse_input(data):
    return np.array([int(x) for x in data.split(',') if x])


class TestClass:
    def test_run_program_1(self):
        registers = parse_input('3,0,4,0,99')
        outputs = run_program(registers, [1])

        assert outputs == [1]


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    outputs = run_program(registers, [1])

    print(outputs[-1])
