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


class NetworkNode():
    def __init__(self, registers):
        self.ip = 0
        self.current_input_index = 0
        self.relative_base = 0
        self.registers = list(registers)
        self.inputs = []
        self.outputs = []

    def empty_queue(self):
        return self.current_input_index >= len(self.inputs)

    def put_messages(self, msg_lst):
        self.inputs += msg_lst

    def get_messages(self):
        N = (len(self.outputs) // 3) * 3

        msg_lst = self.outputs[:N]
        self.outputs = self.outputs[N:]

        return msg_lst

    def run_program(self):
        i = 0

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
            instruction = '0' * 4 + str(self.registers[self.ip])

            opcode = int(instruction[-2:])

            if opcode == 99:
                break

            if opcode == 3:
                if self.current_input_index >= len(self.inputs):
                    self.inputs.append(-1)

                self.ip = operations[opcode](
                    self.ip, instruction, self.relative_base, self.registers,
                    self.inputs[self.current_input_index])

                self.current_input_index += 1

            elif opcode == 4:
                self.ip, output = operations[opcode](
                    self.ip, instruction, self.relative_base, self.registers)

                self.outputs.append(output)

            elif opcode == 9:
                self.ip, self.relative_base = operations[opcode](
                    self.ip, instruction, self.relative_base, self.registers)

            else:
                self.ip = operations[opcode](
                    self.ip, instruction, self.relative_base, self.registers)

            i += 1

            if i == 100:
                break


def run_network(registers, nodes_count, end_addr):
    nodes = []

    for i in range(nodes_count):
        nodes.append(NetworkNode(registers))
        nodes[i].put_messages([i])

    nat_msg = []
    nat_y_set = set()

    done_flag = False

    while True:
        if done_flag:
            break

        sent_count = 0
        empty_queue_count = 0

        for i in range(nodes_count):
            nodes[i].run_program()
            msg_lst = nodes[i].get_messages()

            if len(msg_lst):
                sent_count += 1

            if nodes[i].empty_queue():
                empty_queue_count += 1

            for j in range(0, len(msg_lst), 3):
                addr = msg_lst[j]
                msg = msg_lst[j + 1: j + 3]

                if addr == end_addr:
                    nat_msg = msg
                else:
                    nodes[addr].put_messages(msg)

        if sent_count == 0 and empty_queue_count == nodes_count:
            nodes[0].put_messages(nat_msg)

            if len(nat_msg):
                if nat_msg[1] in nat_y_set:
                    result = nat_msg[1]
                    done_flag = True

                nat_y_set.add(nat_msg[1])

    return result


def parse_input(data):
    data = data.strip()
    return list(map(int, data.split(',')))


if __name__ == '__main__':
    data = sys.stdin.readline()

    registers = parse_input(data)

    result = run_network(registers, 50, 255)
    print(result)
