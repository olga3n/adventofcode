#!/usr/bin/env python3

import sys


def parse_stones(line: str) -> list[int]:
    return list(map(int, line.split()))


def process_one_stone(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)

    if len(str(stone)) % 2 == 0:
        str_stone = str(stone)
        one = int(str_stone[:len(str_stone) // 2])
        two = int(str_stone[len(str_stone) // 2:])
        return (one, two)

    return (stone * 2024, )


def stones_cnt(stones: list[int], iterations: int) -> int:
    freq: dict[int, int] = {}

    for stone in stones:
        freq[stone] = freq.get(stone, 0) + 1

    for _ in range(iterations):
        new_freq: dict[int, int] = {}

        for stone, cnt in freq.items():
            for new_stone in process_one_stone(stone):
                new_freq[new_stone] = new_freq.get(new_stone, 0) + cnt

        freq = new_freq

    return sum(freq.values())


def test_stones_cnt():
    line = '125 17'
    stones = parse_stones(line)

    assert 22 == stones_cnt(stones, iterations=6)
    assert 55312 == stones_cnt(stones, iterations=25)


def main():
    line = sys.stdin.readline()
    result = stones_cnt(parse_stones(line), iterations=75)
    print(result)


if __name__ == '__main__':
    main()
