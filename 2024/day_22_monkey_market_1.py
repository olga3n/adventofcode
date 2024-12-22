#!/usr/bin/env python3

import sys
from typing import Iterable


def next_secret(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def secret_score(lines: Iterable[str], iterations: int = 2000) -> int:
    result = 0
    for line in lines:
        secret = int(line)
        for _ in range(iterations):
            secret = next_secret(secret)
        result += secret
    return result


def test_secret_score():
    lines = [
        '1',
        '10',
        '100',
        '2024',
    ]
    assert 37327623 == secret_score(lines)


def main():
    lines = sys.stdin
    result = secret_score(lines)
    print(result)


if __name__ == '__main__':
    main()
