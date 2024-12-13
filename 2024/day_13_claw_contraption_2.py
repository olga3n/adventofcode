#!/usr/bin/env python3

import sys
from typing import Iterable
from dataclasses import dataclass


@dataclass
class Vec2:
    x: int
    y: int


@dataclass
class ClawData:
    button_a: Vec2
    button_b: Vec2
    prize: Vec2


def parse_data(
    lines: Iterable[str], shift=10000000000000,
) -> Iterable[ClawData]:

    button_a = Vec2(0, 0)
    button_b = Vec2(0, 0)

    for line in lines:
        if line.startswith('Prize:'):
            values = line.split(': ')[1].split(', ')
            value_x = int(values[0].split('=')[1])
            value_y = int(values[1].split('=')[1])
            prize = Vec2(value_x + shift, value_y + shift)
            yield ClawData(button_a, button_b, prize)
        elif line.startswith('Button A:'):
            values = line.split(': ')[1].split(', ')
            value_x = int(values[0].split('+')[1])
            value_y = int(values[1].split('+')[1])
            button_a = Vec2(value_x, value_y)
        elif line.startswith('Button B:'):
            values = line.split(': ')[1].split(', ')
            value_x = int(values[0].split('+')[1])
            value_y = int(values[1].split('+')[1])
            button_b = Vec2(value_x, value_y)


def tokens(claw_data: ClawData) -> int:
    tmp_1 = (
        claw_data.button_a.y * claw_data.prize.x -
        claw_data.button_a.x * claw_data.prize.y
    )
    tmp_2 = (
        claw_data.button_a.y * claw_data.button_b.x -
        claw_data.button_a.x * claw_data.button_b.y
    )
    p2 = tmp_1 // tmp_2

    tmp = claw_data.prize.x - p2 * claw_data.button_b.x
    p1 = tmp // claw_data.button_a.x

    eq1 = p1 * claw_data.button_a.x + p2 * claw_data.button_b.x
    eq2 = p1 * claw_data.button_a.y + p2 * claw_data.button_b.y

    if eq1 == claw_data.prize.x and eq2 == claw_data.prize.y:
        return p1 * 3 + p2

    return 0


def all_tokens(claws: Iterable[ClawData]) -> int:
    return sum(tokens(claw_data) for claw_data in claws)


def test_all_tokens():
    lines = [
        'Button A: X+94, Y+34',
        'Button B: X+22, Y+67',
        'Prize: X=8400, Y=5400',
        '',
        'Button A: X+26, Y+66',
        'Button B: X+67, Y+21',
        'Prize: X=12748, Y=12176',
        '',
        'Button A: X+17, Y+86',
        'Button B: X+84, Y+37',
        'Prize: X=7870, Y=6450',
        '',
        'Button A: X+69, Y+23',
        'Button B: X+27, Y+71',
        'Prize: X=18641, Y=10279',
    ]
    assert 875318608908 == all_tokens(parse_data(lines))


def main():
    lines = sys.stdin
    result = all_tokens(parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()
