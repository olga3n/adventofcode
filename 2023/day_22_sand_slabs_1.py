#!/usr/bin/env python3

import sys
from typing import Iterable
from dataclasses import dataclass


@dataclass
class Block:
    id: int

    x: int
    y: int
    z: int

    dx: int
    dy: int
    dz: int


def parse_blocks(data: Iterable[str]) -> Iterable[Block]:
    for i, line in enumerate(data):
        start, end = line.split('~')
        x1, y1, z1 = list(map(int, start.split(',')))
        x2, y2, z2 = list(map(int, end.split(',')))

        if x2 < x1:
            x1, x2 = x2, x1

        if y2 < y1:
            y1, y2 = y2, y1

        if z2 < z1:
            z1, z2 = z2, z1

        yield Block(i, x1, y1, z1, x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1)


def safe_blocks(data: Iterable[str]) -> int:
    blocks = list(parse_blocks(data))

    max_x = max(max(block.x, block.x + block.dx) for block in blocks)
    max_y = max(max(block.y, block.y + block.dy) for block in blocks)

    heights = []
    last_block = []

    for _ in range(max_x + 1):
        heights.append([1] * (max_y + 1))
        last_block.append([-1] * (max_y + 1))

    deps = {}

    for block in sorted(blocks, key=lambda x: x.z):
        new_z = 0
        for x in range(block.x, block.x + block.dx):
            for y in range(block.y, block.y + block.dy):
                new_z = max(new_z, heights[x][y])
        block.z = new_z
        items = set()
        for x in range(block.x, block.x + block.dx):
            for y in range(block.y, block.y + block.dy):
                if heights[x][y] == new_z and last_block[x][y] != -1:
                    items.add(last_block[x][y])
                heights[x][y] = new_z + block.dz
                last_block[x][y] = block.id
        deps[block.id] = items

    unsafe_blocks = set()

    for block_id, block_deps in deps.items():
        if len(block_deps) == 1:
            for item in block_deps:
                unsafe_blocks.add(item)

    return sum(1 for block in blocks if block.id not in unsafe_blocks)


def test_safe_blocks():
    data = [
        '1,0,1~1,2,1',
        '0,0,2~2,0,2',
        '0,2,3~2,2,3',
        '0,0,4~0,2,4',
        '2,0,5~2,2,5',
        '0,1,6~2,1,6',
        '1,1,8~1,1,9',
    ]
    assert safe_blocks(data) == 5


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = safe_blocks(data)
    print(result)


if __name__ == '__main__':
    main()
