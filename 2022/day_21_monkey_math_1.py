#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node:
    value: Optional[int] = None
    dep_1: Optional[str] = None
    dep_2: Optional[str] = None
    operation: Optional[str] = None


def monkey_number(data: Iterable[str], node_name: str = 'root') -> int:
    nodes = {}

    for line in data:
        name, deps = line.rstrip().split(': ')
        if deps.isdigit():
            nodes[name] = Node(value=int(deps))
        else:
            dep_1, operation, dep_2 = deps.split()
            nodes[name] = Node(dep_1=dep_1, dep_2=dep_2, operation=operation)

    stack = [nodes['root']]

    while stack:
        node = stack.pop()

        if node.value is not None or node.dep_1 is None or node.dep_2 is None:
            continue

        node_1 = nodes[node.dep_1]
        node_2 = nodes[node.dep_2]

        if node_1.value is not None and node_2.value is not None:
            if node.operation == '+':
                node.value = node_1.value + node_2.value
            elif node.operation == '-':
                node.value = node_1.value - node_2.value
            elif node.operation == '*':
                node.value = node_1.value * node_2.value
            elif node.operation == '/':
                node.value = node_1.value // node_2.value
        else:
            stack.extend([node, node_1, node_2])

    return nodes['root'].value if nodes['root'].value else 0


def test_monkey_number():
    data = [
        'root: pppw + sjmn',
        'dbpl: 5',
        'cczh: sllz + lgvd',
        'zczc: 2',
        'ptdq: humn - dvpt',
        'dvpt: 3',
        'lfqf: 4',
        'humn: 5',
        'ljgn: 2',
        'sjmn: drzm * dbpl',
        'sllz: 4',
        'pppw: cczh / lfqf',
        'lgvd: ljgn * ptdq',
        'drzm: hmdt - zczc',
        'hmdt: 32'
    ]

    assert monkey_number(data) == 152


def main():
    data = sys.stdin
    result = monkey_number(data)
    print(result)


if __name__ == '__main__':
    main()
