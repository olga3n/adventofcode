#!/usr/bin/env python3

import sys
import re
import math

import numpy as np


def simulate_motion(moons, velocity):
    velocity_diff = np.zeros(moons.shape)

    for axis in range(0, 3):
        for moon_index_1 in range(0, moons.shape[0]):
            for moon_index_2 in range(0, moons.shape[0]):
                if moon_index_1 != moon_index_2:
                    if moons[moon_index_1][axis] < \
                            moons[moon_index_2][axis]:
                        velocity_diff[moon_index_1][axis] += 1
                    elif moons[moon_index_1][axis] > \
                            moons[moon_index_2][axis]:
                        velocity_diff[moon_index_1][axis] -= 1

    for moon_index in range(0, moons.shape[0]):
        velocity[moon_index] = velocity[moon_index] + velocity_diff[moon_index]
        moons[moon_index] = moons[moon_index] + velocity[moon_index]


def find_repeat(moons):
    moons_first = np.copy(moons)
    velocity = np.zeros(moons.shape)

    full_repeat = 1
    repeated = [0] * moons.shape[1]

    step = 0

    while True:
        simulate_motion(moons, velocity)
        step += 1

        for axis in range(0, 3):
            if repeated[axis] == 0:
                flag_1 = np.array_equal(
                    moons[:, axis],
                    moons_first[:, axis])

                flag_2 = np.array_equal(
                    velocity[:, axis],
                    np.array([0] * moons.shape[0]))

                if flag_1 and flag_2:
                    full_repeat = full_repeat * step // \
                        math.gcd(full_repeat, step)
                    repeated[axis] = 1

        if sum(repeated) == moons.shape[1]:
            break

    return full_repeat


def parse_input(data):
    moons_lst = []

    for line in data:
        line = line.strip()

        m = re.match(r'<x=(.+), y=(.+), z=(.+)>', line)

        if m:
            moons_lst.append(list(map(int, m.groups())))

    return np.array(moons_lst)


class TestClass:
    def test_find_repeat_0(self):
        data = [
            '<x=-1, y=0, z=2>',
            '<x=2, y=-10, z=-7>',
            '<x=4, y=-8, z=8>',
            '<x=3, y=5, z=-1>']

        moons = parse_input(data)

        step = find_repeat(moons)

        assert step == 2772

    def test_find_repeat_1(self):
        data = [
            '<x=-8, y=-10, z=0>',
            '<x=5, y=5, z=10>',
            '<x=2, y=-7, z=3>',
            '<x=9, y=-8, z=-3>']

        moons = parse_input(data)

        step = find_repeat(moons)

        assert step == 4686774924


if __name__ == '__main__':
    data = sys.stdin.readlines()

    moons = parse_input(data)

    step = find_repeat(moons)

    print(step)
