#!/usr/bin/env python3

import sys
import re

import numpy as np


def simulate_motions(moons, velocity, steps):
    for step in range(0, steps):
        for axis in range(0, 3):
            for moon_index_1 in range(0, moons.shape[0]):
                new_velocity = velocity[moon_index_1][axis]

                for moon_index_2 in range(0, moons.shape[0]):
                    if moon_index_1 != moon_index_2:
                        if moons[moon_index_1][axis] < \
                                moons[moon_index_2][axis]:
                            new_velocity += 1
                        elif moons[moon_index_1][axis] > \
                                moons[moon_index_2][axis]:
                            new_velocity -= 1

                velocity[moon_index_1][axis] = new_velocity

        for moon_index in range(0, moons.shape[0]):
            moons[moon_index] = moons[moon_index] + velocity[moon_index]


def calc_kinetic_energy(velocity):
    return np.abs(velocity).sum(axis=1)


def calc_potential_energy(moons):
    return np.abs(moons).sum(axis=1)


def calc_total_energy(moons, steps):

    velocity = np.zeros(moons.shape)

    simulate_motions(moons, velocity, steps)

    kinetic_energy = calc_kinetic_energy(velocity)
    potential_energy = calc_potential_energy(moons)

    return int(np.sum(kinetic_energy * potential_energy))


def parse_input(data):
    moons_lst = []

    for line in data:
        line = line.strip()

        m = re.match(r'<x=(.+), y=(.+), z=(.+)>', line)

        if m:
            moons_lst.append(list(map(int, m.groups())))

    return np.array(moons_lst)


class TestClass:
    def test_calc_total_energy_0(self):
        data = [
            '<x=-1, y=0, z=2>',
            '<x=2, y=-10, z=-7>',
            '<x=4, y=-8, z=8>',
            '<x=3, y=5, z=-1>']

        moons = parse_input(data)

        steps = 10

        total_energy = calc_total_energy(moons, steps)

        assert total_energy == 179

    def test_calc_total_energy_1(self):
        data = [
            '<x=-8, y=-10, z=0>',
            '<x=5, y=5, z=10>',
            '<x=2, y=-7, z=3>',
            '<x=9, y=-8, z=-3>']

        moons = parse_input(data)

        steps = 100

        total_energy = calc_total_energy(moons, steps)

        assert total_energy == 1940


if __name__ == '__main__':
    data = sys.stdin.readlines()

    moons = parse_input(data)
    steps = 1000

    total_energy = calc_total_energy(moons, steps)

    print(total_energy)
