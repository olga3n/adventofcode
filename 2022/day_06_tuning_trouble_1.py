#!/usr/bin/env python3

import sys


def start_of_packet(line: str, uniq_size: int = 4) -> int:
    for i in range(uniq_size, len(line) + 1):
        if len(set(line[i - uniq_size: i])) == uniq_size:
            return i
    return 0


def test_start_of_packet():
    assert start_of_packet('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
    assert start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
    assert start_of_packet('nppdvjthqldpwncqszvftbrmjlhg') == 6
    assert start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
    assert start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11


def main():
    line = sys.stdin.readline()
    result = start_of_packet(line)
    print(result)


if __name__ == '__main__':
    main()
