#!/usr/bin/env python3

import sys
from collections import deque
from typing import Iterable


def next_secret(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def gen_prices(
    secret: int, iterations: int = 2000,
) -> Iterable[tuple[int, int]]:
    prev_price = secret % 10
    for _ in range(iterations):
        secret = next_secret(secret)
        price = secret % 10
        yield price, price - prev_price
        prev_price = price


def best_price(lines: Iterable[str], iterations: int = 2000) -> int:
    options: dict[tuple[int, ...], int] = {}

    for line in lines:
        secret = int(line)
        buyer_options = {}
        seq: deque[int] = deque([])

        for price, diff in gen_prices(secret, iterations):
            seq.append(diff)
            if len(seq) > 4:
                seq.popleft()
            if len(seq) == 4:
                key = tuple(seq)
                if key not in buyer_options:
                    buyer_options[key] = price

        for k, v in buyer_options.items():
            options[k] = options.get(k, 0) + v

    return max(options.values())


def test_best_price():
    lines = [
        '1',
        '2',
        '3',
        '2024',
    ]
    assert 23 == best_price(lines)


def main():
    lines = sys.stdin
    result = best_price(lines)
    print(result)


if __name__ == '__main__':
    main()
