#!/usr/bin/env python3

import sys
import re

import unittest
import textwrap


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

    register_in = []
    command = []
    register_out = []

    for item in data:
        if len(item):
            if 'Before' in item:
                register_in = [int(x) for x in re.findall(r'\d+', item)]
            elif 'After' in item:
                register_out = [int(x) for x in re.findall(r'\d+', item)]

                samples.append([register_in, command, register_out])
            else:
                command = [int(x) for x in item.split(' ')]

    return samples


def opcodes(sample):

    operations = [
        addr, addi,
        mulr, muli,
        banr, bani,
        borr, bori,
        setr, seti,
        gtir, gtri, gtrr,
        eqir, eqri, eqrr
    ]

    register_in, command, register_out = sample

    codes = 0

    for op in operations:
        out = op(command[1:], register_in.copy())

        if out == register_out:
            codes += 1

    return codes


def process(data):
    samples = parse_samples(data)

    result = sum([1 for x in samples if opcodes(x) >= 3])

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            Before: [3, 2, 1, 1]
            9 2 1 2
            After:  [3, 2, 2, 1]
        """).split('\n')

        samples = parse_samples(data)

        self.assertEqual(opcodes(samples[0]), 3)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = process(data)

    print(v)
