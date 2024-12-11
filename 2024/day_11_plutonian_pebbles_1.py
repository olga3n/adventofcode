#!/usr/bin/env python3

import sys


def parse_stones(line: str) -> list[int]:
    return list(map(int, line.split()))


def stones_cnt(stones: list[int], iterations: int) -> int:
    for _ in range(iterations):
        new_stones = []

        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                new_stones.append(int(str_stone[:len(str_stone) // 2]))
                new_stones.append(int(str_stone[len(str_stone) // 2:]))
            else:
                new_stones.append(stone * 2024)

        stones = new_stones

    return len(stones)


def test_stones_cnt():
    line = '125 17'
    stones = parse_stones(line)

    assert 22 == stones_cnt(stones, iterations=6)
    assert 55312 == stones_cnt(stones, iterations=25)


def main():
    line = sys.stdin.readline()
    result = stones_cnt(parse_stones(line), iterations=25)
    print(result)


if __name__ == '__main__':
    main()
