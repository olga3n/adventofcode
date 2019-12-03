#!/usr/bin/env python3

import sys
import numpy as np


def build_matrix(wires):
    min_i, min_j, max_i, max_j = 0, 0, 0, 0

    for path in wires:
        current = np.array([0, 0])

        for delta in path:
            current += delta

            min_i = min(min_i, current[0])
            min_j = min(min_j, current[1])
            max_i = max(max_i, current[0])
            max_j = max(max_j, current[1])

    return (
        np.zeros((max_i - min_i + 1, max_j - min_j + 1)),
        np.array([-min_i, -min_j]))


def find_nearest_intersection_distance(wires):
    m, center = build_matrix(wires)
    min_distance = m.shape[0] + m.shape[1]

    for ind, path in enumerate(wires):
        current = np.copy(center)

        for delta in path:
            one_step = np.array([
                np.sign(delta[0]) * min(1, np.abs(delta[0])),
                np.sign(delta[1]) * min(1, np.abs(delta[1]))])

            seg_start = np.copy(current)

            while not np.array_equal(current, seg_start + delta):
                current += one_step

                if m[tuple(current)] == 0:
                    m[tuple(current)] = ind + 1
                elif m[tuple(current)] != ind + 1 and \
                        not np.array_equal(current, center):

                    distance = np.sum(np.abs(current - center))
                    min_distance = min(min_distance, distance)

    return min_distance


def step_to_vector(step):

    direction = step[0]
    value = int(step[1:])

    if direction == 'U':
        return np.array([-value, 0])
    elif direction == 'D':
        return np.array([value, 0])
    elif direction == 'L':
        return np.array([0, -value])
    elif direction == 'R':
        return np.array([0, value])


def parse_input(data):

    wires = []

    for line in data:
        path = line.strip().split(',')

        if len(path):
            wires.append([step_to_vector(step) for step in path])

    return wires


class TestClass:
    def test_find_nearest_intersection_distance_1(self):
        data = [
            'R8,U5,L5,D3',
            'U7,R6,D4,L4'
        ]

        wires = parse_input(data)
        result = find_nearest_intersection_distance(wires)

        assert result == 6

    def test_find_nearest_intersection_distance_2(self):
        data = [
            'R75,D30,R83,U83,L12,D49,R71,U7,L72',
            'U62,R66,U55,R34,D71,R55,D58,R83'
        ]

        wires = parse_input(data)
        result = find_nearest_intersection_distance(wires)

        assert result == 159

    def test_find_nearest_intersection_distance_3(self):
        data = [
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
        ]

        wires = parse_input(data)
        result = find_nearest_intersection_distance(wires)

        assert result == 135


if __name__ == '__main__':
    data = sys.stdin.readlines()

    wires = parse_input(data)

    result = find_nearest_intersection_distance(wires)

    print(result)
