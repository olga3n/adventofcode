#!/usr/bin/env python3

import sys


def process_answers(data):
    data.append('')

    result = 0
    questions = set()

    for line in data:
        if len(line):
            for x in line:
                questions.add(x)
        else:
            result += len(questions)
            questions = set()

    return result


class TestClass:

    def test_process_answers(self):
        data = [
            'abc',
            '',
            'a',
            'b',
            'c',
            '',
            'ab',
            'ac',
            '',
            'a',
            'a',
            'a',
            'a',
            '',
            'b'
        ]

        assert process_answers(data) == 11


def main():
    data = [line.strip() for line in sys.stdin]
    result = process_answers(data)
    print(result)


if __name__ == '__main__':
    main()
