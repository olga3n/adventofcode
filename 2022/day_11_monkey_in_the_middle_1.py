#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Monkey:
    items: List[int]
    operation_degree_coeff: int = 1
    operation_mult_coeff: int = 1
    operation_add_coeff: int = 0
    div_coeff: int = 1
    true_throw: int = 0
    false_throw: int = 0
    inspected: int = 0


def parse_monkeys(data: Iterable[str]) -> List[Monkey]:
    result = []

    for line in data:
        line = line.strip()

        if line.startswith('Monkey'):
            result.append(Monkey([]))
            continue

        matched = re.match(r'Starting items: (.+)', line)

        if matched:
            result[-1].items = list(map(int, matched.group(1).split(', ')))
            continue

        if line.startswith('Operation: new = old * old'):
            result[-1].operation_degree_coeff = 2
            continue

        matched = re.match(r'.* (\d+)', line)

        if matched:
            value = int(matched.group(1))

            if line.startswith('Operation: new = old *'):
                result[-1].operation_mult_coeff = value
            elif line.startswith('Operation: new = old +'):
                result[-1].operation_add_coeff = value
            elif line.startswith('Test: divisible by'):
                result[-1].div_coeff = value
            elif line.startswith('If true: throw to monkey'):
                result[-1].true_throw = value
            elif line.startswith('If false: throw to monkey'):
                result[-1].false_throw = value

    return result


def monkey_business(data: Iterable[str], rounds: int = 20) -> int:
    monkeys = parse_monkeys(data)

    for round_index in range(rounds):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop()

                item **= monkey.operation_degree_coeff
                item *= monkey.operation_mult_coeff
                item += monkey.operation_add_coeff
                item //= 3

                if item % monkey.div_coeff == 0:
                    monkeys[monkey.true_throw].items.append(item)
                else:
                    monkeys[monkey.false_throw].items.append(item)

                monkey.inspected += 1

    top_monkeys = sorted(monkeys, key=lambda x: -x.inspected)[:2]
    return top_monkeys[0].inspected * top_monkeys[1].inspected


def test_monkey_business():
    data = [
        'Monkey 0:',
        '  Starting items: 79, 98',
        '  Operation: new = old * 19',
        '  Test: divisible by 23',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 3',
        '',
        'Monkey 1:',
        '  Starting items: 54, 65, 75, 74',
        '  Operation: new = old + 6',
        '  Test: divisible by 19',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 0',
        '',
        'Monkey 2:',
        '  Starting items: 79, 60, 97',
        '  Operation: new = old * old',
        '  Test: divisible by 13',
        '    If true: throw to monkey 1',
        '    If false: throw to monkey 3',
        '',
        'Monkey 3:',
        '  Starting items: 74',
        '  Operation: new = old + 3',
        '  Test: divisible by 17',
        '    If true: throw to monkey 0',
        '    If false: throw to monkey 1',
    ]

    assert monkey_business(data) == 10605


def main():
    data = sys.stdin
    result = monkey_business(data)
    print(result)


if __name__ == '__main__':
    main()
