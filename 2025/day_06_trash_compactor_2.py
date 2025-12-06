#!/usr/bin/env python3

import sys
from typing import List
from dataclasses import dataclass


@dataclass
class Expr:
    sign: str
    values: List[int]


def parse_expr(lines: List[str]) -> List[Expr]:
    sign_col_lst = []

    for i, sign in enumerate(lines[-1]):
        if sign != ' ':
            sign_col_lst.append(i)

    result = []

    for i, sign_col in enumerate(sign_col_lst):
        last_expr_col = (
            sign_col_lst[i + 1] - 1
            if i + 1 < len(sign_col_lst) else len(lines[-1])
        )

        values = []

        for col in range(sign_col, last_expr_col):
            value = ''.join(lines[row][col] for row in range(len(lines)-1))
            values.append(int(value))

        result.append(Expr(sign=lines[-1][sign_col], values=values))

    return result


def calculate_expr(sign: str, values: List[int]) -> int:
    result = values[0]

    for i in range(1, len(values)):
        if sign == '+':
            result += values[i]
        elif sign == '*':
            result *= values[i]

    return result


def expressions_sum(expr_list: List[Expr]) -> int:
    return sum(calculate_expr(expr.sign, expr.values) for expr in expr_list)


def test_expressions_sum():
    lines = [
        '123 328  51 64 ',
        ' 45 64  387 23 ',
        '  6 98  215 314',
        '*   +   *   +  ',
    ]
    assert 3263827 == expressions_sum(parse_expr(lines))


def main():
    lines = [line.rstrip('\n') for line in sys.stdin]
    result = expressions_sum(parse_expr(lines))
    print(result)


if __name__ == '__main__':
    main()
