#!/usr/bin/env python3

import sys


def reverse_polish_notation(tokens):
    result = []
    stack = []

    for token in tokens:
        if token.isdigit():
            result.append(int(token))
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while True:
                last_item = stack.pop()

                if last_item == '(':
                    break
                else:
                    result.append(last_item)
        else:
            while True:
                if len(stack) == 0:
                    break

                if stack[-1] == '(':
                    break

                last_item = stack.pop()
                result.append(last_item)

            stack.append(token)

    while len(stack):
        last_item = stack.pop()
        result.append(last_item)

    return result


def eval_expr(expr):
    tokens = [x for x in list(expr) if x != ' ']
    items = reverse_polish_notation(tokens)

    while len(items) > 2:
        for i, item in enumerate(items):
            if item == '+':
                value = items[i - 2] + items[i - 1]
                items = items[:i - 2] + [value] + items[i + 1:]
                break
            elif item == '*':
                value = items[i - 2] * items[i - 1]
                items = items[:i - 2] + [value] + items[i + 1:]
                break

    return items[0]


def sum_expr(data):
    return sum([eval_expr(expr) for expr in data])


class TestClass():

    def test_eval_expr(self):

        expr_1 = '1 + 2 * 3 + 4 * 5 + 6'
        expr_2 = '1 + (2 * 3) + (4 * (5 + 6))'
        expr_3 = '2 * 3 + (4 * 5)'
        expr_4 = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
        expr_5 = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
        expr_6 = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'

        assert eval_expr(expr_1) == 71
        assert eval_expr(expr_2) == 51
        assert eval_expr(expr_3) == 26
        assert eval_expr(expr_4) == 437
        assert eval_expr(expr_5) == 12240
        assert eval_expr(expr_6) == 13632


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = sum_expr(data)
    print(result)


if __name__ == '__main__':
    main()
