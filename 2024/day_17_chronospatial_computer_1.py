#!/usr/bin/env python3

import sys
from typing import Iterable
from dataclasses import dataclass


@dataclass
class Registers:
    a: int
    b: int
    c: int
    ip: int


def parse_data(lines: Iterable[str]) -> tuple[Registers, list[int]]:
    r = Registers(0, 0, 0, 0)
    commands = []

    for line in lines:
        if line.startswith("Register A"):
            r.a = int(line.split(": ")[1])
        elif line.startswith("Register B"):
            r.b = int(line.split(": ")[1])
        elif line.startswith("Register C"):
            r.c = int(line.split(": ")[1])
        elif len(line):
            commands = list(map(int, line.split(": ")[1].split(",")))

    return r, commands


def combo_operand(r: Registers, operand: int) -> int:
    if 0 <= operand <= 3:
        return operand

    if operand == 4:
        return r.a

    if operand == 5:
        return r.b

    if operand == 6:
        return r.c

    return 0


def calc(r: Registers, operation: int, operand: int) -> list[int]:
    if operation == 0:
        r.a = r.a // (2 ** combo_operand(r, operand))
        r.ip += 2
    elif operation == 1:
        r.b = r.b ^ operand
        r.ip += 2
    elif operation == 2:
        r.b = combo_operand(r, operand) % 8
        r.ip += 2
    elif operation == 3:
        if r.a != 0:
            r.ip = operand
        else:
            r.ip += 2
    elif operation == 4:
        r.b = r.b ^ r.c
        r.ip += 2
    elif operation == 5:
        r.ip += 2
        return [combo_operand(r, operand) % 8]
    elif operation == 6:
        r.b = r.a // (2 ** combo_operand(r, operand))
        r.ip += 2
    elif operation == 7:
        r.c = r.a // (2 ** combo_operand(r, operand))
        r.ip += 2

    return []


def process_program(r: Registers, commands: list[int]) -> list[int]:
    out = []

    while r.ip + 1 < len(commands):
        operation = commands[r.ip]
        operand = commands[r.ip + 1]
        out.extend(calc(r, operation, operand))

    return out


def test_process_program():
    r = Registers(0, 0, 9, 0)
    process_program(r, [2, 6])
    assert 1 == r.b

    r = Registers(10, 0, 0, 0)
    out = process_program(r, [5, 0, 5, 1, 5, 4])
    assert [0, 1, 2] == out

    r = Registers(2024, 0, 0, 0)
    out = process_program(r, [0, 1, 5, 4, 3, 0])
    assert [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0] == out
    assert 0 == r.a

    r = Registers(0, 29, 0, 0)
    process_program(r, [1, 7])
    assert 26 == r.b

    r = Registers(0, 2024, 43690, 0)
    process_program(r, [4, 0])
    assert 44354 == r.b


def test_process():
    lines = [
        'Register A: 729',
        'Register B: 0',
        'Register C: 0',
        '',
        'Program: 0,1,5,4,3,0',
    ]
    result = process_program(*parse_data(lines))
    assert "4,6,3,5,6,3,5,2,1,0" == ",".join(map(str, result))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = process_program(*parse_data(lines))
    print(','.join(map(str, result)))


if __name__ == '__main__':
    main()
