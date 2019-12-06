#!/usr/bin/env python3

import sys


def calc_total_orbits(graph):
    orbits = {}

    orbits['COM'] = 0

    current_lst = ['COM']

    while len(current_lst):
        new_lst = []

        for item in current_lst:
            if item in graph:
                for connection in graph[item]:
                    if connection not in orbits:
                        orbits[connection] = orbits[item] + 1
                    else:
                        orbits[connection] = min(
                            orbits[connection], orbits[item] + 1)

                    new_lst.append(connection)

        current_lst = new_lst

    return sum(orbits.values())


def parse_input(data):
    graph = {}

    for line in data:
        line = line.strip()
        obj1, obj2 = line.split(')')

        if obj1 not in graph:
            graph[obj1] = [obj2]
        else:
            graph[obj1].append(obj2)

    return graph


class TestClass:
    def test_calc_total_orbits_1(self):
        data = [
            'COM)B',
            'B)C',
            'C)D',
            'D)E',
            'E)F',
            'B)G',
            'G)H',
            'D)I',
            'E)J',
            'J)K',
            'K)L'
        ]

        graph = parse_input(data)
        result = calc_total_orbits(graph)

        assert result == 42


if __name__ == '__main__':
    data = sys.stdin.readlines()

    graph = parse_input(data)

    result = calc_total_orbits(graph)

    print(result)
