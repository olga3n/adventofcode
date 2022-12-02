#!/usr/bin/env python3

import sys
from typing import Iterable


class Position:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    LOST = 0
    WON = 6
    DRAW = 3


W_COMBINATIONS = {
    (Position.ROCK, Position.PAPER),
    (Position.PAPER, Position.SCISSORS),
    (Position.SCISSORS, Position.ROCK)
}

L_COMBINATIONS = {
    (Position.ROCK, Position.SCISSORS),
    (Position.PAPER, Position.ROCK),
    (Position.SCISSORS, Position.PAPER)
}


def play_round(left: int, right: int) -> int:
    if left == right:
        return right + Position.DRAW
    if (left, right) in W_COMBINATIONS:
        return right + Position.WON
    if (left, right) in L_COMBINATIONS:
        return right + Position.LOST
    return 0


def game_score(data: Iterable[str]) -> int:
    convert = {
        'A': Position.ROCK,
        'B': Position.PAPER,
        'C': Position.SCISSORS,
        'X': Position.ROCK,
        'Y': Position.PAPER,
        'Z': Position.SCISSORS
    }

    return sum(play_round(convert[x[0]], convert[x[-1]]) for x in data if x)


def main() -> None:
    data = (x.strip() for x in sys.stdin.readlines())
    result = game_score(data)
    print(result)


def test_game_score():
    data = [
        'A Y',
        'B X',
        'C Z'
    ]

    assert game_score(data) == 15


if __name__ == '__main__':
    main()
