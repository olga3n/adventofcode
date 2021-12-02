#!/usr/bin/env python3

import sys
from typing import Iterable


class Position:

    def __init__(self, x: int = 0, depth: int = 0):
        self.x = x
        self.depth = depth

    def move_forward(self, value: int) -> None:
        self.x += value

    def move_down(self, value: int) -> None:
        self.depth += value

    def move_up(self, value: int) -> None:
        self.depth -= value


def move_score(data: Iterable[str]) -> int:
    p = Position()

    for line in data:
        cmd, value = line.split()

        if cmd == "forward":
            p.move_forward(int(value))
        elif cmd == "down":
            p.move_down(int(value))
        elif cmd == "up":
            p.move_up(int(value))

    return p.x * p.depth


class TestClass():

    def test_1(self):
        data = [
            "forward 5",
            "down 5",
            "forward 8",
            "up 3",
            "down 8",
            "forward 2"
        ]

        assert move_score(data) == 150


def main():
    data = map(lambda x: x.strip(), sys.stdin)
    result = move_score(data)
    print(result)


if __name__ == '__main__':
    main()
