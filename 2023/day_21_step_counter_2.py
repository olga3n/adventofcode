#!/usr/bin/env python3

import sys
from typing import Tuple, Dict, Set


def process_steps(
    data: Tuple[str],
    block_tiles: Dict[Tuple[int, int], Set[Tuple[int, int]]],
    cnt=1
):
    size = len(data)

    for _ in range(cnt):
        new_block_tiles = {}

        for (block_x, block_y), tiles in block_tiles.items():
            for pos in tiles:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    xx = pos[0] + dx
                    yy = pos[1] + dy
                    block_xx = block_x + xx // size
                    block_yy = block_y + yy // size
                    xx %= size
                    yy %= size
                    if data[xx][yy] == '#':
                        continue
                    if (block_xx, block_yy) not in new_block_tiles:
                        new_block_tiles[(block_xx, block_yy)] = {(xx, yy)}
                    else:
                        new_block_tiles[(block_xx, block_yy)].add((xx, yy))

        block_tiles = new_block_tiles

    return block_tiles


def reachable_tiles(data: Tuple[str], steps: int, start='S') -> int:
    for i, line in enumerate(data):
        j = line.find(start)
        if j >= 0:
            start_pos = (i, j)
            break

    size = len(data)
    block_tiles = {(0, 0): {start_pos}}

    if steps < 5 * size:
        block_tiles = process_steps(data, block_tiles, steps)
        return sum(len(tiles) for tiles in block_tiles.values())

    block_tiles = process_steps(data, block_tiles, steps % size)
    steps -= steps % size

    block_tiles = process_steps(data, block_tiles, size * 4)
    steps -= size * 4

    prev_block_tiles = block_tiles

    block_tiles = process_steps(data, block_tiles, size)
    steps -= size

    border = 7

    freq = {}
    block_key = {}

    for x in range(-border, border + 1):
        for y in range(-border, border + 1):
            value = len(prev_block_tiles.get((x, y), set()))
            env = []
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                env.append(len(prev_block_tiles.get((x + dx, y + dy), set())))
            key = (value, tuple(env))
            if sum(env):
                freq[key] = freq.get(key, 0) + 1
                block_key[(x, y)] = key

    prev_freq = freq
    prev_block_key = block_key

    freq = {}
    block_key = {}

    for x in range(-border, border + 1):
        for y in range(-border, border + 1):
            value = len(block_tiles.get((x, y), set()))
            env = []
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                env.append(len(block_tiles.get((x + dx, y + dy), set())))
            key = (value, tuple(env))
            if sum(env):
                freq[key] = freq.get(key, 0) + 1
                block_key[(x, y)] = key

    full_values = {len(prev_block_tiles[(0, 0)]), len(block_tiles[(0, 0)])}

    diff_cnt = {}

    for key in freq:
        diff_cnt[key] = freq[key] - prev_freq[key]

    value_1, value_2 = full_values

    special_keys = {
        (value_1, (value_2, value_2, value_2, value_2)),
        (value_2, (value_1, value_1, value_1, value_1)),
    }

    full_transitions = {}

    for block, prev_key in prev_block_key.items():
        key = block_key[block]
        if key in special_keys:
            full_transitions[prev_key] = key

    curr_freq = freq

    for _ in range(steps // size):
        new_freq = {}

        for key, value in curr_freq.items():
            if key not in special_keys:
                new_freq[key] = new_freq.get(key, 0) + value + diff_cnt[key]

            if key in full_transitions:
                new_key = full_transitions[key]
                new_freq[new_key] = new_freq.get(new_key, 0) + value

        curr_freq = new_freq

    return sum(key[0] * value for key, value in curr_freq.items())


def test_tiles_count():
    data = [
        '...........',
        '.....###.#.',
        '.###.##..#.',
        '..#.#...#..',
        '....#.#....',
        '.##..S####.',
        '.##..#...#.',
        '.......##..',
        '.##.#.####.',
        '.##..##.##.',
        '...........',
    ]
    assert reachable_tiles(data, steps=6) == 16
    assert reachable_tiles(data, steps=10) == 50
    assert reachable_tiles(data, steps=50) == 1594
    assert reachable_tiles(data, steps=100) == 6536
    assert reachable_tiles(data, steps=500) == 167004
    assert reachable_tiles(data, steps=1000) == 668697
    assert reachable_tiles(data, steps=5000) == 16733044


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = tuple(line for line in data if len(line))
    result = reachable_tiles(data, steps=26501365)
    print(result)


if __name__ == '__main__':
    main()
