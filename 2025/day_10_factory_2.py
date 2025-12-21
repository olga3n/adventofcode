#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple
from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


@dataclass
class Machine:
    target: Tuple[int, ...]
    buttons: List[Tuple[int, ...]]


def parse_lines(lines: Iterable[str]) -> Iterable[Machine]:
    for line in lines:
        parts = line.rstrip().split(' ')
        target: Tuple[int, ...] = tuple()
        buttons = []
        for part in parts:
            if part[0] == '{':
                target = tuple(map(int, part[1:-1].split(',')))
            elif part[0] == '(':
                buttons.append(set(map(int, part[1:-1].split(','))))
        button_profiles = []
        for button in buttons:
            profile = tuple([
                1 if i in button else 0
                for i in range(len(target))
            ])
            button_profiles.append(profile)
        yield Machine(target, button_profiles)


def press(
    values: Tuple[int, ...], button: Tuple[int, ...], cnt=1,
) -> Tuple[int, ...]:
    return tuple([
        value + cnt * button[i]
        for i, value in enumerate(values)
    ])


def min_presses(machine: Machine) -> int:
    A = np.array(machine.buttons).T
    b = np.array(machine.target)
    c = np.ones(len(machine.buttons))

    coeffs = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), integrality=1).x

    values = [0] * len(machine.target)

    for button, coeff in zip(machine.buttons, coeffs):
        values = press(values, button, round(coeff))
        assert round(coeff) >= 0

    assert values == machine.target

    return int(sum(coeffs))


def total_min_presses(machines: Iterable[Machine]) -> int:
    return sum(min_presses(machine) for machine in machines)


def test_total_min_presses():
    lines = [
        '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}',
        '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}',
        '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}',
    ]
    assert 33 == total_min_presses(parse_lines(lines))


def main():
    lines = sys.stdin
    result = total_min_presses(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
