#!/usr/bin/env python3

import sys
import heapq
from typing import List


def max_calories(data: List[str], top_count: int = 3) -> int:
    top_results: List[int] = []
    curr_result = 0

    for i, line in enumerate(data):
        if line:
            curr_result += int(line)

        if not line or (i == len(data) - 1 and curr_result > 0):
            heapq.heappush(top_results, curr_result)
            if len(top_results) > top_count:
                heapq.heappop(top_results)
            curr_result = 0

    return sum(top_results)


def main() -> None:
    data = [x.strip() for x in sys.stdin.readlines()]
    result = max_calories(data)
    print(result)


def test_max_calories():
    data = [
        '1000',
        '2000',
        '3000',
        '',
        '4000',
        '',
        '5000',
        '6000',
        '',
        '7000',
        '8000',
        '9000',
        '',
        '10000',
    ]

    assert max_calories(data) == 45000


if __name__ == '__main__':
    main()
