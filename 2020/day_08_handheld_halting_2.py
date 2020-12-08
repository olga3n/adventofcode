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


def fix_corruption(program):
    commands = parse_commands(program)

    changed_lines = [
        i for i, cmd in enumerate(commands) if cmd[0] in {'nop', 'jmp'}
    ]

    for ind in changed_lines:
        acc, ip = 0, 0
        complete = set()
        status = 'loop'

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
                if ip != ind:
                    ip += value
                else:
                    ip += 1
            else:
                if ip != ind:
                    ip += 1
                else:
                    ip += value

            if ip >= len(commands):
                status = 'done'
                break

        if status == 'done':
            return acc


class TestClass():

    def test_fix_corruption(self):
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

        assert fix_corruption(data) == 8


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = fix_corruption(data)
    print(result)


if __name__ == '__main__':
    main()
