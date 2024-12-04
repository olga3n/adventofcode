#!/usr/bin/env python3

import re
import sys
from typing import Iterable


PATTERN = r'mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don)\'t\(\)'


def parse_lines(lines: Iterable[str]) -> Iterable[tuple[int, int]]:
    flag = True
    for line in lines:
        for group in re.findall(PATTERN, line):
            if group[-1]:
                flag = False

            if group[-2]:
                flag = True

            if flag and not group[-1] and not group[-2]:
                yield (int(group[0]), int(group[1]))


def calculate(lines: Iterable[str]) -> int:
    return sum(group[0] * group[1] for group in parse_lines(lines))


def test_calculate():
    line = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64]" +
        "(mul(12,8)undo()?mul(8,5))"
    )
    assert 48 == calculate([line])


def main():
    lines = sys.stdin
    result = calculate(lines)
    print(result)


if __name__ == '__main__':
    main()
