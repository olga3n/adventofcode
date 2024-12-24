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


def find_best_a_value(r: Registers, commands: list[int]) -> int:
    saved_data = {}

    for a_part in range(1 << 10):
        new_r = Registers(a_part, 0, 0, 0)
        out = process_program(new_r, commands[:-2])

        if out[0] not in saved_data:
            saved_data[out[0]] = [a_part]
        else:
            saved_data[out[0]].append(a_part)

    stack: list[tuple] = [(0, [], saved_data[commands[0]])]
    candidates = set()

    while len(stack):
        index, prev_seq, a_options = stack.pop()
        value = commands[index]

        if index == len(commands) - 1:
            for final_part in a_options:
                buf = prev_seq + [final_part]
                candidate = 0
                for i, value in enumerate(buf):
                    candidate += (value % (1 << 3)) << (3 * i)
                candidates.add(candidate)
            continue

        next_index = index + 1
        next_value = commands[next_index]
        next_a_options = saved_data[next_value]

        for a_part in a_options:
            good_next_a_options = [
                a_next_part
                for a_next_part in next_a_options
                if a_next_part % (1 << 7) == a_part >> 3
            ]
            if len(good_next_a_options):
                seq = prev_seq.copy()
                seq.append(a_part)
                stack.append((next_index, seq, good_next_a_options))

    best_a = min(candidates)
    new_r = Registers(best_a, 0, 0, 0)
    out = process_program(new_r, commands)
    return best_a if out == commands else 0


def test_process():
    lines = [
        'Register A: 2024',
        'Register B: 0',
        'Register C: 0',
        '',
        'Program: 0,3,5,4,3,0',
    ]
    r, commands = parse_data(lines)
    r.a = 117440
    result = process_program(r, commands)
    assert "0,3,5,4,3,0" == ",".join(map(str, result))


def test_find_best_a_value():
    lines = [
        'Register A: 2024',
        'Register B: 0',
        'Register C: 0',
        '',
        'Program: 0,3,5,4,3,0',
    ]
    assert 117440 == find_best_a_value(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = find_best_a_value(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()
