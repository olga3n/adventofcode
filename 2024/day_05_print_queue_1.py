#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Info:
    inverted_rules: dict[int, set[int]]
    updates: list[tuple[int, ...]]


def parse_lines(lines: Iterable[str]) -> Info:
    info = Info(inverted_rules={}, updates=[])

    for line in lines:
        if '|' in line:
            left, right = map(int, line.split('|'))
            if right not in info.inverted_rules:
                info.inverted_rules[right] = {left}
            else:
                info.inverted_rules[right].add(left)
        elif ',' in line:
            update = tuple(map(int, line.split(',')))
            info.updates.append(update)

    return info


def is_correct(
    inverted_rules: dict[int, set[int]], update: tuple[int, ...]
) -> bool:
    invalid_set = set()

    for value in update:
        if value in invalid_set:
            return False

        for invalid_next in inverted_rules.get(value, set()):
            invalid_set.add(invalid_next)

    return True


def right_order_score(info: Info) -> int:
    result = 0

    for update in info.updates:
        if is_correct(info.inverted_rules, update):
            middle_index = len(update) // 2
            result += update[middle_index]

    return result


def test_right_order_score():
    lines = [
        '47|53',
        '97|13',
        '97|61',
        '97|47',
        '75|29',
        '61|13',
        '75|53',
        '29|13',
        '97|29',
        '53|29',
        '61|53',
        '97|53',
        '61|29',
        '47|13',
        '75|47',
        '97|75',
        '47|61',
        '75|61',
        '47|29',
        '75|13',
        '53|13',
        '',
        '75,47,61,53,29',
        '97,61,53,29,13',
        '75,29,13',
        '75,97,47,61,53',
        '61,13,29',
        '97,13,75,29,47',
    ]
    assert 143 == right_order_score(parse_lines(lines))


def main():
    lines = sys.stdin
    result = right_order_score(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
