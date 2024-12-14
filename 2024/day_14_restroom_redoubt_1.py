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


def safety_factor(
    robots: list[Robot], cols: int, rows: int, iterations: int = 100
) -> int:
    for _ in range(iterations):
        for robot in robots:
            robot.pos.x = (robot.pos.x + robot.velocity.x) % cols
            robot.pos.y = (robot.pos.y + robot.velocity.y) % rows

    stat = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}

    for robot in robots:
        if robot.pos.y < rows // 2:
            if robot.pos.x < cols // 2:
                stat['q1'] += 1
            elif robot.pos.x >= (cols + 1) // 2:
                stat['q2'] += 1
        elif robot.pos.y >= (rows + 1) // 2:
            if robot.pos.x < cols // 2:
                stat['q3'] += 1
            elif robot.pos.x >= (cols + 1) // 2:
                stat['q4'] += 1

    result = 1

    for v in stat.values():
        result *= v

    return result


def test_safety_factor():
    lines = [
        'p=0,4 v=3,-3',
        'p=6,3 v=-1,-3',
        'p=10,3 v=-1,2',
        'p=2,0 v=2,-1',
        'p=0,0 v=1,3',
        'p=3,0 v=-2,-2',
        'p=7,6 v=-1,-3',
        'p=3,0 v=-1,-2',
        'p=9,3 v=2,3',
        'p=7,3 v=-1,2',
        'p=2,4 v=2,-3',
        'p=9,5 v=-3,-3',
    ]
    assert 12 == safety_factor(parse_robots(lines), cols=11, rows=7)


def main():
    lines = sys.stdin
    result = safety_factor(parse_robots(lines), cols=101, rows=103)
    print(result)


if __name__ == '__main__':
    main()
