#!/usr/bin/env python3

import sys
from typing import Iterable
from dataclasses import dataclass


@dataclass
class Vec2:
    x: int
    y: int


@dataclass
class Robot:
    pos: Vec2
    velocity: Vec2


def parse_robots(lines: Iterable[str]) -> list[Robot]:
    robots = []

    for line in lines:
        p, v = line.split()
        px, py = map(int, p.split('=')[1].split(','))
        vx, vy = map(int, v.split('=')[1].split(','))
        robots.append(Robot(Vec2(px, py), Vec2(vx, vy)))

    return robots


def build_img(robots: list[Robot], cols: int, rows: int) -> list[str]:
    positions: dict[tuple[int, int], int] = {}

    for robot in robots:
        tuple_pos = (robot.pos.x, robot.pos.y)
        positions[tuple_pos] = positions.get(tuple_pos, 0) + 1

    lines = []
    flag = False

    for y in range(rows):
        line = ''
        for x in range(cols):
            value = str(positions[(x, y)]) if (x, y) in positions else '.'
            line += value

        if '11111111' in line:
            flag = True

        lines.append(line)

    return lines if flag else []


def process(robots: list[Robot], cols: int, rows: int) -> int:
    i = 0

    while True:
        for robot in robots:
            robot.pos.x = (robot.pos.x + robot.velocity.x) % cols
            robot.pos.y = (robot.pos.y + robot.velocity.y) % rows

        lines = build_img(robots, cols, rows)

        for line in lines:
            print(line)

        if lines:
            return i + 1

        i += 1


def main():
    lines = sys.stdin
    result = process(parse_robots(lines), cols=101, rows=103)
    print(result)


if __name__ == '__main__':
    main()
