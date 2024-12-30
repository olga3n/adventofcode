#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable, Union


@dataclass
class Node:
    arg1: Union['Node', None]
    arg2: Union['Node', None]
    operation: str
    leaf: str
    name: str


def parse_lines(lines: Iterable[str]) -> tuple[dict, dict]:
    deps: dict[str, set[str]] = {}
    functions: dict[str, str] = {}

    for line in lines:
        if '->' in line:
            expr, name = line.split(' -> ')
            tokens = expr.split(' ')
            deps[name] = {tokens[0], tokens[2]}
            functions[name] = tokens[1]

    return deps, functions


def one_iteration(deps: dict, functions: dict) -> dict[str, 'Node']:
    mapping_nodes = {}

    for key, args in deps.items():
        arg1, arg2 = args
        if arg1.startswith(('x', 'y')) and arg2.startswith(('x', 'y')):
            if functions[key] == 'XOR':
                k = 'xor{}'.format(arg1[1:])
            elif functions[key] == 'AND':
                k = 'and{}'.format(arg1[1:])
            mapping_nodes[k] = Node(None, None, '', k, key)

    mapping_nodes['z00'] = Node(None, None, '', 'xor00', '')
    mapping_nodes['z01'] = Node(
        mapping_nodes['xor01'], mapping_nodes['and00'], 'XOR', '', '',
    )

    mapping_nodes['zand02'] = Node(
        mapping_nodes['xor01'], mapping_nodes['and00'], 'AND', '', '',
    )
    mapping_nodes['zor02'] = Node(
        mapping_nodes['and01'], mapping_nodes['zand02'], 'OR', '', '',
    )
    mapping_nodes['z02'] = Node(
        mapping_nodes['xor02'], mapping_nodes['zor02'], 'XOR', '', '',
    )

    for i in range(3, 45):
        suffix = str(i).zfill(2)
        suffix_prev = str(i - 1).zfill(2)

        mapping_nodes['zand' + suffix] = Node(
            mapping_nodes['xor' + suffix_prev],
            mapping_nodes['zor' + suffix_prev],
            'AND', '', '',
        )
        mapping_nodes['zor' + suffix] = Node(
            mapping_nodes['and' + suffix_prev],
            mapping_nodes['zand' + suffix],
            'OR', '', '',
        )
        mapping_nodes['z' + suffix] = Node(
            mapping_nodes['xor' + suffix],
            mapping_nodes['zor' + suffix],
            'XOR', '', '',
        )

    mapping_nodes['zand45'] = Node(
        mapping_nodes['xor44'], mapping_nodes['zor44'], 'AND', '', '',
    )
    mapping_nodes['z45'] = Node(
        mapping_nodes['and44'], mapping_nodes['zand45'], 'OR', '', '',
    )

    flag = True

    while flag:
        flag = False
        for node in mapping_nodes.values():
            if node.name == '':
                if node.arg1 is not None and node.arg2 is not None:
                    if node.arg1.name != '' and node.arg2.name != '':
                        dep_set = {node.arg1.name, node.arg2.name}
                        for k, v in deps.items():
                            if v == dep_set and node.operation == functions[k]:
                                node.name = k
                                flag = True
                                break

    return mapping_nodes


def mixed_deps(deps: dict, functions: dict) -> list[str]:
    result = set()

    while True:
        mapping_nodes = one_iteration(deps, functions)

        pairs = []

        for k, v in sorted(mapping_nodes.items()):
            if k[0] == 'z' and not k.startswith(('zor', 'zand')):
                if v.name != '' and v.name[0] != 'z':
                    pairs.append((k, v.name))

        if len(pairs) == 0:
            z_next = 'z46'
            for k, v in sorted(mapping_nodes.items()):
                if k[0] == 'z' and not k.startswith(('zor', 'zand')):
                    if v.name == '' and k != 'z00':
                        z_next = min(k, z_next)

            if z_next != 'z46':
                arg1 = mapping_nodes[z_next].arg1
                arg2 = mapping_nodes[z_next].arg2
                if arg1 is not None and arg2 is not None:
                    if arg1.name != '' and arg2.name != '':
                        diff = tuple(deps[z_next].symmetric_difference(
                            {arg1.name, arg2.name}
                        ))
                        pairs.append((diff[0], diff[1]))

        if len(pairs) == 0:
            break

        for key1, key2 in pairs:
            deps[key1], deps[key2] = deps[key2], deps[key1]
            functions[key1], functions[key2] = functions[key2], functions[key1]
            result.add(key1)
            result.add(key2)

    return sorted(result)


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = mixed_deps(*parse_lines(lines))
    print(','.join(result))


if __name__ == '__main__':
    main()
