#!/usr/bin/env python3

import sys
from typing import Dict, Iterable, List, Tuple


def parse_lines(lines: Iterable[str]) -> List[Tuple[int, ...]]:
    positions = []

    for line in lines:
        values = line.rstrip().split(',')
        positions.append(tuple(map(int, values)))

    return positions


def calc_distances(
    positions: List[Tuple[int, ...]],
) -> Dict[Tuple[int, int], int]:

    distances = {}

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            distances[(i, j)] = (
                (positions[i][0] - positions[j][0]) ** 2 +
                (positions[i][1] - positions[j][1]) ** 2 +
                (positions[i][2] - positions[j][2]) ** 2
            )

    return distances


def last_connection(positions: List[Tuple[int, ...]]) -> Tuple[int, int]:
    distances = calc_distances(positions)
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    circuits = [i for i in range(len(positions))]
    last_i, last_j = 0, 0

    for (index_1, index_2), _ in sorted_distances:
        if circuits[index_1] != circuits[index_2]:
            last_i, last_j = index_1, index_2
            prev_circuit = circuits[index_2]
            for i in range(len(circuits)):
                if circuits[i] == prev_circuit:
                    circuits[i] = circuits[index_1]

        if len(set(circuits)) == 1:
            break

    return last_i, last_j


def circuit_score(
    positions: List[Tuple[int, ...]],
) -> int:
    last_i, last_j = last_connection(positions)
    return positions[last_i][0] * positions[last_j][0]


def test_circuit_score():
    lines = [
        '162,817,812',
        '57,618,57',
        '906,360,560',
        '592,479,940',
        '352,342,300',
        '466,668,158',
        '542,29,236',
        '431,825,988',
        '739,650,466',
        '52,470,668',
        '216,146,977',
        '819,987,18',
        '117,168,530',
        '805,96,715',
        '346,949,466',
        '970,615,88',
        '941,993,340',
        '862,61,35',
        '984,92,344',
        '425,690,689',
    ]
    assert 25272 == circuit_score(parse_lines(lines))


def main():
    lines = sys.stdin
    result = circuit_score(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
