#!/usr/bin/env python3

import sys
from typing import List, Dict


def polymer_score(data: List[str], steps: int = 40) -> int:

    pattern = data[0]
    rules = {}

    for line in data[1:]:
        if '->' in line:
            src, dst = line.split(' -> ')
            rules[src] = dst

    stat = {}

    for i in range(len(pattern) - 1):
        stat[pattern[i: i + 2]] = stat.get(pattern[i: i + 2], 0) + 1

    for step in range(steps):
        new_stat: Dict[str, int] = {}

        for p in stat:
            part_1 = p[0] + rules[p]
            part_2 = rules[p] + p[1]
            new_stat[part_1] = new_stat.get(part_1, 0) + stat[p]
            new_stat[part_2] = new_stat.get(part_2, 0) + stat[p]

        stat = new_stat

    freq: Dict[str, int] = {}

    for p in stat:
        freq[p[0]] = freq.get(p[0], 0) + stat[p]
        freq[p[1]] = freq.get(p[1], 0) + stat[p]

    for letter in freq:
        if letter == pattern[0] or letter == pattern[-1]:
            freq[letter] = (freq[letter] + 1) // 2
        else:
            freq[letter] //= 2

    sorted_freq = sorted(freq.values(), reverse=True)

    return sorted_freq[0] - sorted_freq[-1]


class TestClass():

    def test_1(self):
        data = [
            'NNCB',
            '',
            'CH -> B',
            'HH -> N',
            'CB -> H',
            'NH -> C',
            'HB -> C',
            'HC -> B',
            'HN -> C',
            'NN -> C',
            'BH -> H',
            'NC -> B',
            'NB -> B',
            'BN -> B',
            'BB -> N',
            'BC -> B',
            'CC -> N',
            'CN -> C',
        ]

        assert polymer_score(data) == 2188189693529


def main():
    data = [x.strip() for x in sys.stdin]
    result = polymer_score(data)
    print(result)


if __name__ == '__main__':
    main()
