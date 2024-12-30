#!/usr/bin/env python3

import sys
from typing import Callable, Iterable


def parse_lines(lines: Iterable[str]) -> tuple[dict, dict, dict]:
    signals: dict[str, int] = {}
    deps: dict[str, set[str]] = {}
    functions: dict[str, Callable[[int, int], int]] = {}

    for line in lines:
        if ':' in line:
            name, value = line.split(': ')
            signals[name] = int(value)
        elif '->' in line:
            expr, name = line.split(' -> ')
            tokens = expr.split(' ')
            deps[name] = {tokens[0], tokens[2]}
            if tokens[1] == 'AND':
                functions[name] = lambda x, y: x & y
            elif tokens[1] == 'OR':
                functions[name] = lambda x, y: x | y
            elif tokens[1] == 'XOR':
                functions[name] = lambda x, y: x ^ y

    return signals, deps, functions


def calc_output(signals: dict, deps: dict, functions: dict) -> int:
    targets = {name for name in deps if name.startswith('z')}

    while not all(name in signals for name in targets):
        for name, dep_set in deps.items():
            if all(n in signals for n in dep_set):
                args = [signals[n] for n in dep_set]
                signals[name] = functions[name](*args)

    result = 0

    for i, name in enumerate(sorted(targets)):
        result += signals[name] << i

    return result


def test_calc_output():
    lines = [
        'x00: 1',
        'x01: 0',
        'x02: 1',
        'x03: 1',
        'x04: 0',
        'y00: 1',
        'y01: 1',
        'y02: 1',
        'y03: 1',
        'y04: 1',
        '',
        'ntg XOR fgs -> mjb',
        'y02 OR x01 -> tnw',
        'kwq OR kpj -> z05',
        'x00 OR x03 -> fst',
        'tgd XOR rvg -> z01',
        'vdt OR tnw -> bfw',
        'bfw AND frj -> z10',
        'ffh OR nrd -> bqk',
        'y00 AND y03 -> djm',
        'y03 OR y00 -> psh',
        'bqk OR frj -> z08',
        'tnw OR fst -> frj',
        'gnj AND tgd -> z11',
        'bfw XOR mjb -> z00',
        'x03 OR x00 -> vdt',
        'gnj AND wpb -> z02',
        'x04 AND y00 -> kjc',
        'djm OR pbm -> qhw',
        'nrd AND vdt -> hwm',
        'kjc AND fst -> rvg',
        'y04 OR y02 -> fgs',
        'y01 AND x02 -> pbm',
        'ntg OR kjc -> kwq',
        'psh XOR fgs -> tgd',
        'qhw XOR tgd -> z09',
        'pbm OR djm -> kpj',
        'x03 XOR y03 -> ffh',
        'x00 XOR y04 -> ntg',
        'bfw OR bqk -> z06',
        'nrd XOR fgs -> wpb',
        'frj XOR qhw -> z04',
        'bqk OR frj -> z07',
        'y03 OR x01 -> nrd',
        'hwm AND bqk -> z03',
        'tgd XOR rvg -> z12',
        'tnw OR pbm -> gnj',
    ]
    assert 2024 == calc_output(*parse_lines(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = calc_output(*parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
