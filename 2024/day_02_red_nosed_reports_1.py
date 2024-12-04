#!/usr/bin/env python3

import sys
from typing import Iterable


def parse_lines(lines: Iterable[str]) -> Iterable[list[int]]:
    for line in lines:
        yield list(map(int, line.split()))


def safe_report(report: list[int]) -> bool:
    if len(report) < 2:
        return True

    is_increasing = report[0] < report[1]

    for i in range(len(report) - 1):
        if is_increasing:
            if not 0 < report[i + 1] - report[i] < 4:
                return False
        else:
            if not 0 < report[i] - report[i + 1] < 4:
                return False

    return True


def safe_reports(reports: Iterable[list[int]]) -> int:
    return sum(1 for report in reports if safe_report(report))


def test_safe_report():
    lines = [
        '7 6 4 2 1',
        '1 2 7 8 9',
        '9 7 6 2 1',
        '1 3 2 4 5',
        '8 6 4 4 1',
        '1 3 6 7 9',
    ]
    assert 2 == safe_reports(parse_lines(lines))


def main():
    lines = sys.stdin
    result = safe_reports(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
