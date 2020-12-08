#!/usr/bin/env python3

import sys


def parse_commands(program):
    result = []

    for line in program:
        operation, value = line.split(' ')

        if value[0] == '+':
            value = int(value[1:])
        else:
            value = -int(value[1:])

        result.append((operation, value))

    return result


def find_loop(program):
    commands = parse_commands(program)

    acc, ip = 0, 0
    complete = set()

    while True:
        if ip in complete:
            break
        else:
            complete.add(ip)

        operation, value = commands[ip]

        if operation == 'acc':
            acc += value
            ip += 1
        elif operation == 'jmp':
            ip += value
        else:
            ip += 1

    return acc


class TestClass():

    def test_find_loop(self):
        data = [
            'nop +0',
            'acc +1',
            'jmp +4',
            'acc +3',
            'jmp -3',
            'acc -99',
            'acc +1',
            'jmp -4',
            'acc +6'
        ]

        assert find_loop(data) == 5


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = find_loop(data)
    print(result)


if __name__ == '__main__':
    main()
