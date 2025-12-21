#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple, Set
from dataclasses import dataclass
from collections import deque


toggle_dict = {
    '.': '#',
    '#': '.',
}


@dataclass
class Machine:
    target: Tuple[str, ...]
    buttons: List[Set[int]]


def parse_lines(lines: Iterable[str]) -> Iterable[Machine]:
    for line in lines:
        parts = line.rstrip().split(' ')
        target: Tuple[str, ...] = tuple()
        buttons = []
        for part in parts:
            if part[0] == '[':
                target = tuple(part[1:-1])
            elif part[0] == '(':
                buttons.append(set(map(int, part[1:-1].split(','))))
        yield Machine(target, buttons)


def press(lights: Tuple[str, ...], button: Set[int]) -> Tuple[str, ...]:
    return tuple([
        light if i not in button else toggle_dict[light]
        for i, light in enumerate(lights)
    ])


def min_presses(machine: Machine) -> int:
    lights = tuple(['.'] * len(machine.target))
    queue = deque([(lights, -1, 0)])

    while queue:
        lights, last_press, presses = queue.popleft()

        if lights == machine.target:
            return presses

        for i in range(max(0, last_press), len(machine.buttons)):
            next_lights = press(lights, machine.buttons[i])
            queue.append((next_lights, i, presses + 1))

    return -1


def total_min_presses(machines: Iterable[Machine]) -> int:
    return sum(min_presses(machine) for machine in machines)


def test_total_min_presses():
    lines = [
        '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}',
        '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}',
        '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}',
    ]
    assert 7 == total_min_presses(parse_lines(lines))


def main():
    lines = sys.stdin
    result = total_min_presses(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
