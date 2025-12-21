#!/usr/bin/env python3

import sys
from typing import Dict, Iterable, Set
from dataclasses import dataclass


@dataclass
class State:
    none: Dict[str, int]
    fft: Dict[str, int]
    dac: Dict[str, int]
    both: Dict[str, int]

    def none_add(self, key: str, value: int):
        self.none[key] = self.none.get(key, 0) + value

    def fft_add(self, key: str, value: int):
        self.fft[key] = self.fft.get(key, 0) + value

    def dac_add(self, key: str, value: int):
        self.dac[key] = self.dac.get(key, 0) + value

    def both_add(self, key: str, value: int):
        self.both[key] = self.both.get(key, 0) + value


def parse_lines(lines: Iterable[str]) -> Dict[str, Set[str]]:
    graph = {}

    for line in lines:
        line = line.rstrip()
        part_1, part_2 = line.split(': ')
        graph[part_1] = set(part_2.split())

    return graph


def all_paths(
    graph: Dict[str, Set[str]], start='svr', end='out',
) -> int:

    dp = State(none={start: 1}, fft={}, dac={}, both={})

    result = 0

    while len(dp.none) or len(dp.fft) or len(dp.dac) or len(dp.both):

        dp_new = State(none={}, fft={}, dac={}, both={})

        for v_in in dp.none:
            if v_in not in graph:
                continue
            for v_out in graph[v_in]:
                if v_out == 'fft':
                    dp_new.fft_add(v_out, dp.none[v_in])
                elif v_out == 'dac':
                    dp_new.dac_add(v_out, dp.none[v_in])
                else:
                    dp_new.none_add(v_out, dp.none[v_in])

        for v_in in dp.fft:
            if v_in not in graph:
                continue
            for v_out in graph[v_in]:
                if v_out == 'dac':
                    dp_new.both_add(v_out, dp.fft[v_in])
                else:
                    dp_new.fft_add(v_out, dp.fft[v_in])

        for v_in in dp.dac:
            if v_in not in graph:
                continue
            for v_out in graph[v_in]:
                if v_out == 'fft':
                    dp_new.both_add(v_out, dp.dac[v_in])
                else:
                    dp_new.dac_add(v_out, dp.dac[v_in])

        for v_in in dp.both:
            if v_in not in graph:
                continue
            for v_out in graph[v_in]:
                dp_new.both_add(v_out, dp.both[v_in])

        dp = dp_new
        result += dp.both.get(end, 0)

    return result


def test_all_paths():
    lines = [
        'svr: aaa bbb',
        'aaa: fft',
        'fft: ccc',
        'bbb: tty',
        'tty: ccc',
        'ccc: ddd eee',
        'ddd: hub',
        'hub: fff',
        'eee: dac',
        'dac: fff',
        'fff: ggg hhh',
        'ggg: out',
        'hhh: out',
    ]
    assert 2 == all_paths(parse_lines(lines))


def main():
    lines = sys.stdin
    result = all_paths(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
