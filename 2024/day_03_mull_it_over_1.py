#!/usr/bin/env python3

import re
import sys
from typing import Iterable


MUL_REGEXP = r'mul\((\d{1,3}),(\d{1,3})\)'


def parse_line(line: str) -> Iterable[tuple[int, ...]]:
    for matched in re.finditer(MUL_REGEXP, line):
        values = tuple(map(int, matched.groups()))
        yield values


def calculate(lines: Iterable[str]) -> int:
    return sum(
        group[0] * group[1]
        for line in lines
        for group in parse_line(line)
    )


def test_calculate():
    line = (
        'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]' +
        'then(mul(11,8)mul(8,5))'
    )
    assert 161 == calculate([line])


def main():
    lines = sys.stdin
    result = calculate(lines)
    print(result)


if __name__ == '__main__':
    main()
