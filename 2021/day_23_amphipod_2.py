#!/usr/bin/env python3

import sys
from typing import List, Tuple, Set


ENERGY = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

CANDIDATES = {
    'A': ((5, 3), (4, 3), (3, 3), (2, 3)),
    'B': ((5, 5), (4, 5), (3, 5), (2, 5)),
    'C': ((5, 7), (4, 7), (3, 7), (2, 7)),
    'D': ((5, 9), (4, 9), (3, 9), (2, 9))
}

HALL_CANDIDATES = (
    (1, 1),
    (1, 2),
    (1, 4),
    (1, 6),
    (1, 8),
    (1, 10),
    (1, 11)
)


def check_path(
    data: Tuple[str, ...], pos1: Tuple[int, int], pos2: Tuple[int, int]
) -> Tuple[int, Tuple[str, ...]]:

    i, j = pos1
    i0, j0 = pos1
    i1, j1 = pos2

    size = 0

    while i > i1:
        i -= 1
        if data[i][j] != '.':
            return -1, data
        size += 1

    while j1 > j:
        j += 1
        if data[i][j] != '.':
            return -1, data
        size += 1

    while j > j1:
        j -= 1
        if data[i][j] != '.':
            return -1, data
        size += 1

    while i1 > i:
        i += 1
        if data[i][j] != '.':
            return -1, data
        size += 1

    new_data = []

    for ind, row in enumerate(data):
        if ind == i1:
            row = row[:j1] + data[i0][j0] + row[j1 + 1:]
        if ind == i0:
            row = row[:j0] + '.' + row[j0 + 1:]

        new_data.append(row)

    return size * ENERGY[data[i0][j0]], tuple(new_data)


def optimal_path_score(data: List[str]) -> int:
    patch = [
        '  #D#C#B#A#',
        '  #D#B#A#C#',
    ]

    table = tuple(data[:3] + patch + data[3:])

    ready = 0

    for symbol, positions in CANDIDATES.items():
        for i, j in positions:
            if table[i][j] == symbol:
                ready += ENERGY[symbol]
            else:
                break

    states_dict = {(ready, 0): [table]}
    result = -1
    used: Set[Tuple[str, ...]] = set()

    while len(states_dict):
        ready, score = min(states_dict.keys(), key=lambda x: x[1])
        table = states_dict[(ready, score)].pop()

        if len(states_dict[(ready, score)]) == 0:
            states_dict.pop((ready, score))

        if result != -1 and score > result:
            continue

        if table in used:
            continue

        used.add(table)

        if ready == 4444:
            if result == -1 or result > score:
                result = score
            continue

        flag = False

        for j, symbol in enumerate(table[1]):
            if symbol.isalpha():
                for pos in CANDIDATES[symbol]:
                    i0, j0 = pos
                    if table[i0][j0] == symbol:
                        continue
                    if table[i0][j0] != '.':
                        break
                    new_score, new_table = check_path(table, (1, j), (i0, j0))
                    if new_score != -1:
                        table = new_table
                        score = new_score + score
                        ready += ENERGY[new_table[i0][j0]]
                        flag = True
                    break

        if flag and (result == -1 or result > score):
            if (ready, score) in states_dict:
                states_dict[(ready, score)].append(table)
            else:
                states_dict[(ready, score)] = [table]
            continue

        for i in range(2, 6):
            for j, symbol in enumerate(table[i]):
                if symbol.isalpha():
                    if table[i - 1][j] != '.':
                        continue
                    if j == CANDIDATES[symbol][0][1]:
                        ready_status = True
                        for pos in CANDIDATES[symbol]:
                            i0, j0 = pos
                            if i0 < i:
                                break
                            if table[i0][j0] != symbol:
                                ready_status = False
                                break
                        if ready_status:
                            continue
                    for i0, j0 in HALL_CANDIDATES:
                        if table[i0][j0] != '.':
                            continue
                        new_score, new_table = check_path(
                            table, (i, j), (i0, j0)
                        )
                        if new_score != -1:
                            key = (ready, score + new_score)
                            if result == -1 or result > key[1]:
                                if key in states_dict:
                                    states_dict[key].append(new_table)
                                else:
                                    states_dict[key] = [new_table]

    return result


class TestClass():

    def test_1(self):
        data = [
            '#############',
            '#...........#',
            '###B#C#B#D###',
            '  #A#D#C#A#',
            '  #########',
        ]
        assert optimal_path_score(data) == 44169


def main():
    data = [x.strip('\n') for x in sys.stdin]
    result = optimal_path_score(data)
    print(result)


if __name__ == '__main__':
    main()
