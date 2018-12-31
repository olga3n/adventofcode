#!/usr/bin/env python3

import sys
import re

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def run_code(data):

    operations = {
        'addr': addr, 'addi': addi,
        'mulr': mulr, 'muli': muli,
        'banr': banr, 'bani': bani,
        'borr': borr, 'bori': bori,
        'setr': setr, 'seti': seti,
        'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
        'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr
    }

    registers = [0] * 6
    ip_reg = 0

    code_lines = []

    for line in data:
        cmd, args = line.split(' ', 1)
        args = [int(x) for x in args.split(' ')]

        if cmd == '#ip':
            ip_reg = args[0]
        else:
            code_lines.append((cmd, args))

    while True:
        ip_val = registers[ip_reg]

        if ip_val < len(code_lines):

            cmd, args = code_lines[ip_val]

            logging.info(
                "ip: %02.d, cmd: %s, args: %s, registers: %s" %
                (ip_val, cmd, args, registers))

            if cmd[-1] != 'r' or (args[0] != 0 and args[1] != 0):
                registers = operations[cmd](args, registers)

                if registers[ip_reg] < len(code_lines) - 1:
                    registers[ip_reg] += 1
                else:
                    break
            else:
                if cmd == 'eqrr':
                    registers[args[1]] = registers[args[0]]
                    registers[args[2]] = 1

                if registers[ip_reg] < len(code_lines) - 1:
                    registers[ip_reg] += 1
                else:
                    break
        else:
            break

    return registers


def process(data):
    registers = run_code(data)

    return registers[0]


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = process(data)

    print(v)
