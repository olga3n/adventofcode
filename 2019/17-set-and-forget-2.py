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


def run_program(registers, inputs=None):
    outputs = []

    ip = 0
    current_input_index = 0
    relative_base = 0

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
            break

        if opcode == 3:
            ip = operations[opcode](
                ip, instruction, relative_base, registers,
                inputs[current_input_index])

            current_input_index += 1

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

    return outputs


def adj_scaffold(lines, pos):
    scaffold = []

    ii, jj = pos

    if ii > 0 and lines[ii - 1][jj] == '#':
        scaffold.append((ii - 1, jj))

    if ii < len(lines) - 1 and lines[ii + 1][jj] == '#':
        scaffold.append((ii + 1, jj))

    if jj > 0 and lines[ii][jj - 1] == '#':
        scaffold.append((ii, jj - 1))

    if jj < len(lines[ii]) - 1 and lines[ii][jj + 1] == '#':
        scaffold.append((ii, jj + 1))

    return scaffold


def build_path(registers):
    outputs = run_program(registers)

    lines = ''.join([chr(item) for item in outputs]).strip()

    lines = lines.split('\n')

    robot_pos = (-1, -1)
    robot_view = '^'

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] not in {'#', '.'}:
                robot_pos = (i, j)
                robot_view = lines[i][j]
                break

    robot_turns = {
        '^': {
            (-1, 0): ('', '^'),
            (0, -1): ('L', '<'),
            (0, 1): ('R', '>')},
        'v': {
            (1, 0): ('', 'v'),
            (0, 1): ('L', '>'),
            (0, -1): ('R', '<')},
        '<': {
            (0, -1): ('', '<'),
            (1, 0): ('L', 'v'),
            (-1, 0): ('R', '^')},
        '>': {
            (0, 1): ('', '>'),
            (-1, 0): ('L', '^'),
            (1, 0): ('R', 'v')}}

    path = []

    prev_pos = (-1, -1)

    while True:
        sc_lst = \
            [item for item in adj_scaffold(lines, robot_pos)
                if item != prev_pos]

        if len(sc_lst) == 1:
            ii, jj = sc_lst[0]
            i, j = robot_pos

            di, dj = (ii - i, jj - j)
            robot_turn, robot_view = robot_turns[robot_view][(di, dj)]

            step = 0

            while True:
                if not 0 <= i + di <= len(lines) - 1 or \
                        not 0 <= j + dj <= len(lines[i + di]) - 1 or \
                        lines[i + di][j + dj] != '#':
                    break

                prev_pos = (i, j)
                i, j = (i + di, j + dj)
                step += 1

            robot_pos = (i, j)

            if robot_turn:
                path.append(robot_turn)

            path.append(str(step))
        else:
            break

    return path


def build_functions(path):
    tmp_path = list(path)

    new_tmp_path = []

    index = 0

    while index <= len(tmp_path) - 1:
        if index < len(tmp_path) - 1 and \
                tmp_path[index] in {'L', 'R'}:
            new_tmp_path.append(
                (tmp_path[index], tmp_path[index + 1]))
            index += 2
        else:
            new_tmp_path.append((tmp_path[index],))
            index += 1

    tmp_path = new_tmp_path

    while len(set(tmp_path)) != 3:
        tmp_stat = {}

        for i in range(len(tmp_path) - 1):
            part = tmp_path[i] + tmp_path[i + 1]

            if part not in tmp_stat:
                tmp_stat[part] = 1
            else:
                tmp_stat[part] += 1

        top_freq = sorted(
            tmp_stat.items(), key=lambda x: x[1], reverse=True)[0][0]

        new_tmp_path = []

        index = 0

        while index <= len(tmp_path) - 1:
            if index < len(tmp_path) - 1 and \
                    tmp_path[index] + tmp_path[index + 1] == top_freq:
                new_tmp_path.append(top_freq)
                index += 2
            else:
                new_tmp_path.append(tmp_path[index])
                index += 1

        tmp_path = new_tmp_path

    A, B, C = set(tmp_path)

    functions = {'A': A, 'B': B, 'C': C}

    new_tmp_path = []

    for item in tmp_path:
        if item == A:
            new_tmp_path.append('A')
        if item == B:
            new_tmp_path.append('B')
        if item == C:
            new_tmp_path.append('C')

    return functions, new_tmp_path


def space_dust_amount(registers):
    path = build_path(list(registers))

    functions, new_path = build_functions(path)

    registers[0] = 2

    path_lst = ','.join(new_path) + '\n'

    func_a = ','.join(functions['A']) + '\n'
    func_b = ','.join(functions['B']) + '\n'
    func_c = ','.join(functions['C']) + '\n'

    input_lst = path_lst + func_a + func_b + func_c + 'y\n'
    input_lst = [ord(ch) for ch in input_lst]

    outputs = run_program(registers, inputs=input_lst)

    space_dust = outputs[-1]

    return space_dust


def parse_input(data):
    data = data.strip()
    return list(map(int, data.split(',')))


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    result = space_dust_amount(registers)
    print(result)
