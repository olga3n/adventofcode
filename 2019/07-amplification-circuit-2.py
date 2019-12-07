#!/usr/bin/env python3

import sys
import itertools
import numpy as np


class Amplifier:
    def __init__(self, phase, registers):
        self.ip = 0
        self.registers = registers
        self.inputs = [phase]
        self.input_index = 0
        self.outputs = []
        self.is_done = False

    def add_input(self, value):
        self.inputs.append(value)
        self.gen_next_signal()

    def gen_next_signal(self):
        while True:
            instruction = '0' * 4 + str(self.registers[self.ip])

            opcode = int(instruction[-2:])

            ax_mode = int(instruction[-3])
            bx_mode = int(instruction[-4])
            cx_mode = int(instruction[-5])

            if 1 <= opcode <= 2:
                ax = self.registers[self.ip + 1]
                bx = self.registers[self.ip + 2]
                cx = self.registers[self.ip + 3]

                arg1 = self.registers[ax] if ax_mode == 0 else ax
                arg2 = self.registers[bx] if bx_mode == 0 else bx

                if opcode == 1:
                    self.registers[cx] = arg1 + arg2
                elif opcode == 2:
                    self.registers[cx] = arg1 * arg2

                self.ip += 4

            elif 3 <= opcode <= 4:
                ax = self.registers[self.ip + 1]

                if opcode == 3:
                    if len(self.inputs) > self.input_index:
                        self.registers[ax] = self.inputs[self.input_index]
                        self.input_index += 1
                    else:
                        break

                elif opcode == 4:
                    arg1 = self.registers[ax] if ax_mode == 0 else ax
                    self.outputs.append(arg1)

                self.ip += 2

            elif 5 <= opcode <= 6:
                ax = self.registers[self.ip + 1]
                bx = self.registers[self.ip + 2]

                arg1 = self.registers[ax] if ax_mode == 0 else ax
                arg2 = self.registers[bx] if bx_mode == 0 else bx

                if opcode == 5:
                    self.ip = arg2 if arg1 != 0 else self.ip + 3
                elif opcode == 6:
                    self.ip = arg2 if arg1 == 0 else self.ip + 3

            elif 7 <= opcode <= 8:
                ax = self.registers[self.ip + 1]
                bx = self.registers[self.ip + 2]
                cx = self.registers[self.ip + 3]

                arg1 = self.registers[ax] if ax_mode == 0 else ax
                arg2 = self.registers[bx] if bx_mode == 0 else bx

                if opcode == 7:
                    self.registers[cx] = 1 if arg1 < arg2 else 0
                elif opcode == 8:
                    self.registers[cx] = 1 if arg1 == arg2 else 0

                self.ip += 4

            elif opcode == 99:
                self.is_done = True
                break


def max_signal(registers):
    max_signal = 0
    best_settings = [5, 6, 7, 8, 9]

    for settings in itertools.permutations([5, 6, 7, 8, 9]):
        amplifiers = []

        for i in range(0, 5):
            a_i = Amplifier(settings[i], np.copy(registers))
            amplifiers.append(a_i)

        signal = 0

        while True:
            for i in range(0, 5):
                amplifiers[i].add_input(signal)
                output = amplifiers[i].outputs[-1]
                signal = output

            if amplifiers[-1].is_done:
                break

        if signal > max_signal:
            max_signal = signal
            best_settings = list(settings)

    return max_signal, best_settings


def parse_input(data):
    return np.array([int(x) for x in data.split(',') if x])


class TestClass:
    def test_max_signal_1(self):
        registers = parse_input(
            '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,'
            '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')

        result, settings = max_signal(registers)

        assert (result == 139629729) and (settings == [9, 8, 7, 6, 5])

    def test_max_signal_2(self):
        registers = parse_input(
            '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,'
            '54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,'
            '53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')

        result, settings = max_signal(registers)

        assert (result == 18216) and (settings == [9, 7, 8, 5, 6])


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    result, _ = max_signal(registers)

    print(result)
