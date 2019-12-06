#!/usr/bin/env python3

import sys


def calc_minimum_transfers(graph):
    orbits = {}
    visited = set()

    orbits['YOU'] = 0

    current_lst = ['YOU']

    while len(current_lst):
        new_lst = []

        for item in current_lst:
            if item in graph and item not in visited:
                for connection in graph[item]:
                    if connection not in orbits:
                        orbits[connection] = orbits[item] + 1
                    else:
                        orbits[connection] = min(
                            orbits[connection], orbits[item] + 1)

                    new_lst.append(connection)

                visited.add(item)

        current_lst = new_lst

    return orbits['SAN'] - 2


def parse_input(data):
    graph = {}

    for line in data:
        line = line.strip()
        obj1, obj2 = line.split(')')

        if obj1 not in graph:
            graph[obj1] = [obj2]
        elif obj2 not in graph[obj1]:
            graph[obj1].append(obj2)

        if obj2 not in graph:
            graph[obj2] = [obj1]
        elif obj1 not in graph[obj2]:
            graph[obj2].append(obj1)

    return graph


class TestClass:
    def test_calc_minimum_transfers_1(self):
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
            'K)L',
            'K)YOU',
            'I)SAN'
        ]

        graph = parse_input(data)
        result = calc_minimum_transfers(graph)

        assert result == 4


if __name__ == '__main__':
    data = sys.stdin.readlines()

    graph = parse_input(data)

    result = calc_minimum_transfers(graph)

    print(result)
