#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple
from dataclasses import dataclass


@dataclass
class Region:
    size_x: int
    size_y: int
    figures_cnt: List[int]


@dataclass
class Figure:
    figure: List[str]
    score: int


def parse_lines(lines: Iterable[str]) -> Tuple[List[Figure], List[Region]]:
    figures, regions = [], []
    figure: List[str] = []

    for line in lines:
        if len(line) == 0:
            figures.append(Figure(figure, 0))
            figure = []
        elif 'x' in line:
            left, right = line.split(': ')
            x, y = left.split('x')
            figures_cnt = list(map(int, right.split()))
            region = Region(int(x), int(y), figures_cnt)
            regions.append(region)
        elif ':' not in line:
            figure.append(line)

    return figures, regions


def check_region(region: Region, figures: List[Figure]) -> bool:
    if (region.size_x // 3) * (region.size_y // 3) >= sum(region.figures_cnt):
        return True

    filled = sum(
        figures[i].score * cnt for i, cnt in enumerate(region.figures_cnt)
    )

    if filled > region.size_x * region.size_y:
        return False

    assert False


def good_regions(figures: List[Figure], regions: List[Region]) -> int:
    for figure in figures:
        figure.score = sum(line.count('#') for line in figure.figure)

    return sum(1 for region in regions if check_region(region, figures))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = good_regions(*parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()
