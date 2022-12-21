#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node:
    value: Optional[int] = None
    dep_1: Optional[str] = None
    dep_2: Optional[str] = None
    operation: Optional[str] = None
    expression: Optional[str] = None


def root_expression(data: Iterable[str], node_name: str = 'root') -> str:
    nodes = {}

    for line in data:
        name, deps = line.rstrip().split(': ')
        if name == 'humn':
            nodes[name] = Node(expression='x')
        elif deps.isdigit():
            nodes[name] = Node(value=int(deps), expression=deps)
        else:
            dep_1, operation, dep_2 = deps.split()
            nodes[name] = Node(dep_1=dep_1, dep_2=dep_2, operation=operation)
            if name == 'root':
                nodes[name].operation = '-'

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
            node.expression = str(node.value)
        elif node_1.expression is not None and node_2.expression is not None:
            node.expression = (
                f'({node_1.expression}) {node.operation} ({node_2.expression})'
            )
        else:
            stack.extend([node, node_1, node_2])

    return nodes['root'].expression if nodes['root'].expression else ''


def find_number(data: Iterable[str]) -> int:
    expression = root_expression(data)

    result = 0

    reg_exp_1 = r'\(([-\d]+)\) (.) \((.+)\)'
    reg_exp_2 = r'\((.+)\) (.) \(([-\d]+)\)'

    while expression != 'x':
        m1 = re.match(reg_exp_1, expression)

        if m1:
            arg_1, op, arg_2 = m1.groups()
        else:
            m2 = re.match(reg_exp_2, expression)
            if not m2:
                break
            arg_1, op, arg_2 = m2.groups()

        if arg_1.isdigit():
            if op == '+':
                result -= int(arg_1)
                expression = arg_2
            elif op == '-':
                result = - (result - int(arg_1))
                expression = arg_2
            elif op == '*':
                result //= int(arg_1)
                expression = arg_2
            elif op == '/':
                expression = f'({arg_2}) * ({result})'
                result = int(arg_1)
        elif arg_2.isdigit():
            if op == '+':
                result -= int(arg_2)
            elif op == '-':
                result += int(arg_2)
            elif op == '*':
                result //= int(arg_2)
            elif op == '/':
                result *= int(arg_2)
            expression = arg_1

    return result


def test_find_number():
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

    assert find_number(data) == 301


def main():
    data = sys.stdin
    result = find_number(data)
    print(result)


if __name__ == '__main__':
    main()
