#!/usr/bin/env python3

import sys
import re


def shuffling(stages, N):
    cards = list(range(N))

    for stage in stages:
        cards = stage(cards)

    return cards


def stage_new_stack(cards):
    return cards[::-1]


def stage_cut(cards, value):
    return cards[value:] + cards[:value]


def stage_increment(cards, value):
    new_cards = list(cards)

    index = 0

    for i in range(len(cards)):
        new_cards[index] = cards[i]
        index = (index + value) % len(cards)

    return new_cards


def parse_input(data):
    data = [x.strip() for x in data if len(x.strip())]

    stages = []

    for line in data:
        m1 = re.match(r'deal into new stack', line)
        m2 = re.match(r'cut (.+)', line)
        m3 = re.match(r'deal with increment (.+)', line)

        if m1:
            stages.append(stage_new_stack)
        elif m2:
            v = int(m2[1])
            stages.append(lambda x, v=v: stage_cut(x, v))
        elif m3:
            v = int(m3[1])
            stages.append(lambda x, v=v: stage_increment(x, v))

    return stages


class TestClass:
    def test_shuffling_0(self):
        data = [
            'deal with increment 7',
            'deal into new stack',
            'deal into new stack']

        stages = parse_input(data)

        result = shuffling(stages, 10)

        assert result == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

    def test_shuffling_1(self):
        data = [
            'cut 6',
            'deal with increment 7',
            'deal into new stack']

        stages = parse_input(data)

        result = shuffling(stages, 10)

        assert result == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

    def test_shuffling_2(self):
        data = [
            'deal with increment 7',
            'deal with increment 9',
            'cut -2']

        stages = parse_input(data)

        result = shuffling(stages, 10)

        assert result == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

    def test_shuffling_3(self):
        data = [
            'deal into new stack',
            'cut -2',
            'deal with increment 7',
            'cut 8',
            'cut -4',
            'deal with increment 7',
            'cut 3',
            'deal with increment 9',
            'deal with increment 3',
            'cut -1']

        stages = parse_input(data)

        result = shuffling(stages, 10)

        assert result == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]


if __name__ == '__main__':
    data = sys.stdin.readlines()

    stages = parse_input(data)

    result = shuffling(stages, 10007).index(2019)

    print(result)
