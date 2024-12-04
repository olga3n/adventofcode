#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Status:
    orig: bool
    fixed_asc: bool
    fixed_desc: bool


def parse_lines(lines: Iterable[str]) -> Iterable[list[int]]:
    for line in lines:
        yield list(map(int, line.split()))


def safe_cmp(report: list[int], i: int, j: int, desc=False) -> bool:
    if desc:
        i, j = j, i
    return 0 < report[j] - report[i] < 4


def safe_report(report: list[int]) -> bool:
    if len(report) < 3:
        return True

    statuses = [Status(False, False, False) for i in range(len(report))]

    desc = report[0] > report[1]

    statuses[0].orig = True

    statuses[1].fixed_asc = True
    statuses[1].fixed_desc = True

    if safe_cmp(report, 0, 2):
        statuses[2].fixed_asc = True

    if safe_cmp(report, 0, 2, desc=True):
        statuses[2].fixed_desc = True

    for i in range(1, len(report)):
        if statuses[i - 1].orig:
            statuses[i].orig = safe_cmp(report, i - 1, i, desc=desc)

            if i < len(report) - 1:
                if not desc and not statuses[i + 1].fixed_asc:
                    statuses[i + 1].fixed_asc = safe_cmp(
                        report, i - 1, i + 1, desc=False
                    )

                if desc and not statuses[i + 1].fixed_desc:
                    statuses[i + 1].fixed_desc = safe_cmp(
                        report, i - 1, i + 1, desc=True
                    )

        if statuses[i - 1].fixed_asc and not statuses[i].fixed_asc:
            statuses[i].fixed_asc = safe_cmp(report, i - 1, i, desc=False)

        if statuses[i - 1].fixed_desc and not statuses[i].fixed_desc:
            statuses[i].fixed_desc = safe_cmp(report, i - 1, i, desc=True)

    return (
        statuses[-1].orig or statuses[-2].orig or
        statuses[-1].fixed_asc or statuses[-1].fixed_desc
    )


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
    assert 4 == safe_reports(parse_lines(lines))


def main():
    lines = sys.stdin
    result = safe_reports(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
