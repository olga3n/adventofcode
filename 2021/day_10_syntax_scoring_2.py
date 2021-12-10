#!/usr/bin/env python3

import sys
from typing import List


def line_scoring(line: str) -> int:
    pairs = {"]": "[", ")": "(", ">": "<", "}": "{"}
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}

    bracket_stack = []

    for symbol in line:
        if symbol in {"(", "[", "{", "<"}:
            bracket_stack.append(symbol)
        elif pairs[symbol] == bracket_stack[-1]:
            bracket_stack.pop()
        else:
            return 0

    result = 0

    while len(bracket_stack):
        symbol = bracket_stack.pop()
        result = result * 5 + scores[symbol]

    return result


def middle_scoring(data: List[str]) -> int:
    scores = [line_scoring(line) for line in data]
    scores = sorted([score for score in scores if score != 0])
    return scores[len(scores) // 2]


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

        assert middle_scoring(data) == 288957


def main():
    data = [x.strip() for x in sys.stdin]
    result = middle_scoring(data)
    print(result)


if __name__ == '__main__':
    main()
