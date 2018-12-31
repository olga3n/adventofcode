#!/usr/bin/env python3

import sys
import re


def addr(args, registers):
    registers[args[2]] = registers[args[0]] + registers[args[1]]
    return registers


def addi(args, registers):
    registers[args[2]] = registers[args[0]] + args[1]
    return registers


def mulr(args, registers):
    registers[args[2]] = registers[args[0]] * registers[args[1]]
    return registers


def muli(args, registers):
    registers[args[2]] = registers[args[0]] * args[1]
    return registers


def banr(args, registers):
    registers[args[2]] = registers[args[0]] & registers[args[1]]
    return registers


def bani(args, registers):
    registers[args[2]] = registers[args[0]] & args[1]
    return registers


def borr(args, registers):
    registers[args[2]] = registers[args[0]] | registers[args[1]]
    return registers


def bori(args, registers):
    registers[args[2]] = registers[args[0]] | args[1]
    return registers


def setr(args, registers):
    registers[args[2]] = registers[args[0]]
    return registers


def seti(args, registers):
    registers[args[2]] = args[0]
    return registers


def gtir(args, registers):
    registers[args[2]] = 1 if args[0] > registers[args[1]] else 0
    return registers


def gtri(args, registers):
    registers[args[2]] = 1 if registers[args[0]] > args[1] else 0
    return registers


def gtrr(args, registers):
    registers[args[2]] = 1 if registers[args[0]] > registers[args[1]] else 0
    return registers


def eqir(args, registers):
    registers[args[2]] = 1 if args[0] == registers[args[1]] else 0
    return registers


def eqri(args, registers):
    registers[args[2]] = 1 if registers[args[0]] == args[1] else 0
    return registers


def eqrr(args, registers):
    registers[args[2]] = 1 if registers[args[0]] == registers[args[1]] else 0
    return registers


def parse_samples(data):
    samples = []
    test = []

    register_in = []
    command = []
    register_out = []

    sample_flag = False

    for item in data:
        if len(item):
            values = [int(x) for x in re.findall(r'\d+', item)]

            if 'Before' in item:
                register_in = values
                sample_flag = True
            elif 'After' in item:
                register_out = values
                sample_flag = False

                samples.append([register_in, command, register_out])
            elif sample_flag:
                command = values
            else:
                test.append(values)

    return samples, test


def process(data):
    samples, test = parse_samples(data)

    operations = [
        addr, addi,
        mulr, muli,
        banr, bani,
        borr, bori,
        setr, seti,
        gtir, gtri, gtrr,
        eqir, eqri, eqrr
    ]

    d = {}

    for sample in samples:
        register_in, command, register_out = sample

        for op in operations:
            out = op(command[1:], register_in.copy())

            if out == register_out:
                if command[0] not in d:
                    d[command[0]] = [op]
                else:
                    d[command[0]].append(op)

    for k in d.keys():
        d[k] = list(set(d[k]))

    op_dict = {}
    n = len(d.keys())

    for i in range(n):
        new_op = [k for k, v in d.items() if len(v) == 1]

        for op in new_op:
            op_dict[op] = d[op][0]
            d.pop(op, None)

            for k in d.keys():
                d[k] = [v for v in d[k] if v != op_dict[op]]

    registers = [0, 0, 0, 0]

    for cmd in test:
        f = op_dict[cmd[0]]
        args = cmd[1:]

        registers = f(args, registers)

    return registers[0]


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = process(data)

    print(v)
