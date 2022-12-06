#!/usr/bin/env python3

import sys
from typing import Dict


def first_marker(line: str, uniq_size: int = 14) -> int:
    freq: Dict[str, int] = {}

    for i in range(len(line)):
        freq[line[i]] = freq.get(line[i], 0) + 1
        if i >= uniq_size:
            prev_symbol = line[i - uniq_size]
            freq[prev_symbol] -= 1
            if freq[prev_symbol] == 0:
                freq.pop(prev_symbol)
        if len(freq) == uniq_size:
            return i + 1

    return 0


def test_start_of_packet():
    assert first_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19
    assert first_marker('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23
    assert first_marker('nppdvjthqldpwncqszvftbrmjlhg') == 23
    assert first_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29
    assert first_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26


def main():
    line = sys.stdin.readline()
    result = first_marker(line)
    print(result)


if __name__ == '__main__':
    main()
