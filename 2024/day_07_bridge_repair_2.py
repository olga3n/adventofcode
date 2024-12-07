#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class EqData:
    target: int
    values: list[int]


def parse_lines(lines: Iterable[str]) -> Iterable[EqData]:
    for line in lines:
        left, right = line.split(': ')
        values = list(map(int, right.split()))
        yield EqData(int(left), values)


def gen_options(curr_value: int, next_arg: int) -> Iterable[int]:
    yield curr_value + next_arg
    yield curr_value * next_arg
    yield int(str(curr_value) + str(next_arg))


def is_correct(sample: EqData) -> bool:
    options = {sample.values[0]}

    for i in range(1, len(sample.values)):
        options = {
            new_option
            for option in options
            for new_option in gen_options(option, sample.values[i])
            if new_option <= sample.target
        }

    return sample.target in options


def correct_sum(samples: Iterable[EqData]) -> int:
    return sum(sample.target for sample in samples if is_correct(sample))


def test_correct_sum():
    lines = [
        '190: 10 19',
        '3267: 81 40 27',
        '83: 17 5',
        '156: 15 6',
        '7290: 6 8 6 15',
        '161011: 16 10 13',
        '192: 17 8 14',
        '21037: 9 7 18 13',
        '292: 11 6 16 20',
    ]
    assert 11387 == correct_sum(parse_lines(lines))


def main():
    lines = sys.stdin
    result = correct_sum(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
