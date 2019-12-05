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


def parse_input(data):
    return np.array([int(x) for x in data.split(',') if x])


class TestClass:
    def test_run_program_1(self):
        registers = parse_input('3,9,8,9,10,9,4,9,99,-1,8')
        outputs = run_program(registers, [8])

        assert outputs == [1]

    def test_run_program_2(self):
        registers = parse_input('3,9,8,9,10,9,4,9,99,-1,8')
        outputs = run_program(registers, [1])

        assert outputs == [0]

    def test_run_program_3(self):
        registers = parse_input('3,9,7,9,10,9,4,9,99,-1,8')
        outputs = run_program(registers, [7])

        assert outputs == [1]

    def test_run_program_4(self):
        registers = parse_input('3,9,7,9,10,9,4,9,99,-1,8')
        outputs = run_program(registers, [9])

        assert outputs == [0]

    def test_run_program_5(self):
        registers = parse_input('3,3,1108,-1,8,3,4,3,99')
        outputs = run_program(registers, [8])

        assert outputs == [1]

    def test_run_program_6(self):
        registers = parse_input('3,3,1108,-1,8,3,4,3,99')
        outputs = run_program(registers, [1])

        assert outputs == [0]

    def test_run_program_7(self):
        registers = parse_input('3,3,1107,-1,8,3,4,3,99')
        outputs = run_program(registers, [7])

        assert outputs == [1]

    def test_run_program_8(self):
        registers = parse_input('3,3,1107,-1,8,3,4,3,99')
        outputs = run_program(registers, [9])

        assert outputs == [0]

    def test_run_program_9(self):
        registers = parse_input('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9')
        outputs = run_program(registers, [0])

        assert outputs == [0]

    def test_run_program_10(self):
        registers = parse_input('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9')
        outputs = run_program(registers, [1])

        assert outputs == [1]

    def test_run_program_11(self):
        registers = parse_input('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')
        outputs = run_program(registers, [0])

        assert outputs == [0]

    def test_run_program_12(self):
        registers = parse_input('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')
        outputs = run_program(registers, [1])

        assert outputs == [1]

    def test_run_program_13(self):
        registers = parse_input(
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,'
            '0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,'
            '20,4,20,1105,1,46,98,99')

        outputs = run_program(registers, [7])

        assert outputs == [999]

    def test_run_program_14(self):
        registers = parse_input(
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,'
            '0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,'
            '20,4,20,1105,1,46,98,99')

        outputs = run_program(registers, [8])

        assert outputs == [1000]

    def test_run_program_15(self):
        registers = parse_input(
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,'
            '0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,'
            '20,4,20,1105,1,46,98,99')

        outputs = run_program(registers, [9])

        assert outputs == [1001]


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    outputs = run_program(registers, [5])

    print(outputs[-1])
