#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple


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


def parse_monkeys(data: Iterable[str]) -> Tuple[List[Monkey], List[int]]:
    monkeys: List[Monkey] = []
    items: List[int] = []

    for line in data:
        line = line.strip()

        if line.startswith('Monkey'):
            monkeys.append(Monkey([]))
            continue

        matched = re.match(r'Starting items: (.+)', line)

        if matched:
            monkey_items = list(map(int, matched.group(1).split(', ')))
            for item in monkey_items:
                monkeys[-1].items.append(len(items))
                items.append(item)
            continue

        if line.startswith('Operation: new = old * old'):
            monkeys[-1].operation_degree_coeff = 2
            continue

        matched = re.match(r'.* (\d+)', line)

        if matched:
            value = int(matched.group(1))

            if line.startswith('Operation: new = old *'):
                monkeys[-1].operation_mult_coeff = value
            elif line.startswith('Operation: new = old +'):
                monkeys[-1].operation_add_coeff = value
            elif line.startswith('Test: divisible by'):
                monkeys[-1].div_coeff = value
            elif line.startswith('If true: throw to monkey'):
                monkeys[-1].true_throw = value
            elif line.startswith('If false: throw to monkey'):
                monkeys[-1].false_throw = value

    return monkeys, items


def monkey_business(data: Iterable[str], rounds: int = 10000) -> int:
    monkeys, items = parse_monkeys(data)
    div_coeffs = {monkey.div_coeff for monkey in monkeys}
    items_reminders = []

    for item in items:
        reminders = {}
        for coeff in div_coeffs:
            reminders[coeff] = item % coeff
        items_reminders.append(reminders)

    for round_index in range(rounds):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop()

                for coeff, reminder in items_reminders[item].items():
                    reminder **= monkey.operation_degree_coeff
                    reminder %= coeff
                    reminder *= monkey.operation_mult_coeff
                    reminder %= coeff
                    reminder += monkey.operation_add_coeff
                    reminder %= coeff

                    items_reminders[item][coeff] = reminder

                if items_reminders[item][monkey.div_coeff] == 0:
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

    assert monkey_business(data) == 2713310158


def main():
    data = sys.stdin
    result = monkey_business(data)
    print(result)


if __name__ == '__main__':
    main()
