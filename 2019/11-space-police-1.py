#!/usr/bin/env python3

import sys


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


def run_program_for_current_panel(ip, relative_base, registers, inputs=None):
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


def painted_panels_count(registers):

    painted_panels = 0

    panel_colors = {}

    current_panel = (0, 0)
    current_dir = (-1, 0)

    rotations = {
            (-1, 0): {
                0: (0, -1),
                1: (0, 1)},
            (1, 0): {
                0: (0, 1),
                1: (0, -1)},
            (0, -1): {
                0: (1, 0),
                1: (-1, 0)},
            (0, 1): {
                0: (-1, 0),
                1: (1, 0)}
        }

    ip = 0
    relative_base = 0

    while True:
        is_new_panel = False

        if current_panel not in panel_colors:
            panel_colors[current_panel] = 0

            is_new_panel = True

        current_color = panel_colors[current_panel]

        ip, relative_base, outputs = run_program_for_current_panel(
            ip, relative_base, registers, [current_color])

        if ip == -1:
            break

        color, direction = outputs

        panel_colors[current_panel] = color

        current_dir = rotations[current_dir][direction]
        current_panel = (
            current_panel[0] + current_dir[0],
            current_panel[1] + current_dir[1])

        if is_new_panel:
            painted_panels += 1

    return painted_panels


def parse_input(data):
    data = data.strip()
    return list(map(int, data.split(',')))


if __name__ == '__main__':
    data = sys.stdin.readline()
    registers = parse_input(data)

    result = painted_panels_count(registers)

    print(result)
