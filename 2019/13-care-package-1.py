#!/usr/bin/env python3

import sys
import numpy as np


def resolve_arg(instruction, relative_base, index, registers, ip):

    ax_mode = int(instruction[-3 - index])

    if ax_mode == 0:
        ax = registers[ip + 1 + index]
        ax_type = 'position'
    elif ax_mode == 1:
        ax = registers[ip + 1 + index]
        ax_type = 'value'
    elif ax_mode == 2:
        ax = relative_base + registers[ip + 1 + index]
        ax_type = 'position'

    if ax_type == 'position':
        while len(registers) <= ax:
            registers.append(0)

    return (ax_type, ax)


def operation_add(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)
    cx_type, cx = resolve_arg(instruction, relative_base, 2, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    registers[cx] = arg1 + arg2

    return ip + 4


def operation_mul(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)
    cx_type, cx = resolve_arg(instruction, relative_base, 2, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    registers[cx] = arg1 * arg2

    return ip + 4


def operation_get_input(
        ip, instruction, relative_base, registers, input_value):

    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)

    registers[ax] = input_value

    return ip + 2


def operation_set_output(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax

    return (ip + 2, arg1)


def operation_jump_if_true(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    return arg2 if arg1 != 0 else ip + 3


def operation_jump_if_false(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    return arg2 if arg1 == 0 else ip + 3


def operation_less_than(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)
    cx_type, cx = resolve_arg(instruction, relative_base, 2, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    registers[cx] = 1 if arg1 < arg2 else 0

    return ip + 4


def operation_equals(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)
    bx_type, bx = resolve_arg(instruction, relative_base, 1, registers, ip)
    cx_type, cx = resolve_arg(instruction, relative_base, 2, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax
    arg2 = registers[bx] if bx_type == 'position' else bx

    registers[cx] = 1 if arg1 == arg2 else 0

    return ip + 4


def operation_set_relative_base(ip, instruction, relative_base, registers):
    ax_type, ax = resolve_arg(instruction, relative_base, 0, registers, ip)

    arg1 = registers[ax] if ax_type == 'position' else ax

    return (ip + 2, relative_base + arg1)


def run_program(ip, relative_base, registers, inputs=None):
    outputs = []

    current_input_index = 0

    operations = {
        1: operation_add,
        2: operation_mul,
        3: operation_get_input,
        4: operation_set_output,
        5: operation_jump_if_true,
        6: operation_jump_if_false,
        7: operation_less_than,
        8: operation_equals,
        9: operation_set_relative_base
    }

    while True:
        instruction = '0' * 4 + str(registers[ip])

        opcode = int(instruction[-2:])

        if opcode == 99:
            ip = -1
            break

        if opcode == 3:
            if current_input_index < len(inputs):
                ip = operations[opcode](
                    ip, instruction, relative_base, registers,
                    inputs[current_input_index])

                current_input_index += 1
            else:
                break

        elif opcode == 4:
            ip, output = operations[opcode](
                ip, instruction, relative_base, registers)

            outputs.append(output)

        elif opcode == 9:
            ip, relative_base = operations[opcode](
                ip, instruction, relative_base, registers)

        else:
            ip = operations[opcode](
                ip, instruction, relative_base, registers)

    return ip, relative_base, outputs


def build_game(registers):
    ip = 0
    relative_base = 0

    ip, relative_base, outputs = run_program(ip, relative_base, registers)

    max_x = 0
    max_y = 0

    for ind in range(0, len(outputs), 3):
        max_x = max(max_x, outputs[ind])
        max_y = max(max_y, outputs[ind + 1])

    board = np.zeros((max_y + 1, max_x + 1))

    for ind in range(0, len(outputs), 3):
        xi, yi, v = outputs[ind: ind + 3]

        board[yi][xi] = v

    return board


def calc_block_tiles(registers):
    board = build_game(registers)

    return board[board == 2].shape[0]


def parse_input(data):
    data = data.strip()
    return list(map(int, data.split(',')))


if __name__ == '__main__':
    data = sys.stdin.readline()
    registers = parse_input(data)

    result = calc_block_tiles(registers)

    print(result)
