#!/usr/bin/env python3

import sys
import re
from typing import List, Tuple


def parse_stacks(data: List[str]) -> List[List[str]]:
    stacks = []

    for index, line in enumerate(data):
        if not line:
            break

    for col in range(1, len(data[index - 2]), 4):
        stack = []

        for row in range(index - 2, -1, -1):
            if data[row][col] != ' ':
                stack.append(data[row][col])

        stacks.append(stack)

    return stacks


def parse_rules(data: List[str]) -> List[Tuple[int, ...]]:
    rules = []

    for line in data:
        matched = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        if matched:
            rules.append(tuple(map(int, matched.groups())))

    return rules


def top_stacks_value(data: List[str]) -> str:
    stacks = parse_stacks(data)
    rules = parse_rules(data)

    for cnt, ind_from, ind_to in rules:
        stacks[ind_to - 1].extend(stacks[ind_from - 1][-cnt:])
        stacks[ind_from - 1] = stacks[ind_from - 1][:-cnt]

    return ''.join([stack.pop() for stack in stacks])


def test_top_stacks_value():
    data = [
        '    [D]    ',
        '[N] [C]    ',
        '[Z] [M] [P]',
        ' 1   2   3 ',
        '',
        'move 1 from 2 to 1',
        'move 3 from 1 to 3',
        'move 2 from 2 to 1',
        'move 1 from 1 to 2',
    ]

    assert top_stacks_value(data) == 'MCD'


def main():
    data = [x.rstrip('\n') for x in sys.stdin.readlines()]
    result = top_stacks_value(data)
    print(result)


if __name__ == '__main__':
    main()
