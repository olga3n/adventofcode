#!/usr/bin/env python3

import sys
from typing import List


def line_scoring(line: str) -> int:
    pairs = {"]": "[", ")": "(", ">": "<", "}": "{"}
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    bracket_stack = []

    for symbol in line:
        if symbol in {"(", "[", "{", "<"}:
            bracket_stack.append(symbol)
        elif pairs[symbol] == bracket_stack[-1]:
            bracket_stack.pop()
        else:
            return scores[symbol]

    return 0


def scoring(data: List[str]) -> int:
    return sum([line_scoring(line) for line in data])


class TestClass():

    def test_1(self):
        data = [
            '[({(<(())[]>[[{[]{<()<>>',
            '[(()[<>])]({[<{<<[]>>(',
            '{([(<{}[<>[]}>{[]{[(<()>',
            '(((({<>}<{<{<>}{[]{[]{}',
            '[[<[([]))<([[{}[[()]]]',
            '[{[{({}]{}}([{[{{{}}([]',
            '{<[[]]>}<{[{[{[]{()[[[]',
            '[<(<(<(<{}))><([]([]()',
            '<{([([[(<>()){}]>(<<{{',
            '<{([{{}}[<[[[<>{}]]]>[]]',
        ]

        assert scoring(data) == 26397


def main():
    data = [x.strip() for x in sys.stdin]
    result = scoring(data)
    print(result)


if __name__ == '__main__':
    main()
