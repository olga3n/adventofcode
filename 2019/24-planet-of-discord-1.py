#!/usr/bin/env python3

import sys


def adj_bugs(state, i, j):
    bugs = 0

    if i > 0 and state[i - 1][j] == '#':
        bugs += 1

    if i < len(state) - 1 and state[i + 1][j] == '#':
        bugs += 1

    if j > 0 and state[i][j - 1] == '#':
        bugs += 1

    if j < len(state[i]) - 1 and state[i][j + 1] == '#':
        bugs += 1

    return bugs


def next_state(state):
    new_state = []

    for i in range(len(state)):
        new_line = ''

        for j in range(len(state[i])):
            if state[i][j] == '#':
                if adj_bugs(state, i, j) != 1:
                    new_line += '.'
                else:
                    new_line += '#'
            if state[i][j] == '.':
                if 1 <= adj_bugs(state, i, j) <= 2:
                    new_line += '#'
                else:
                    new_line += '.'

        new_state.append(new_line)

    return new_state


def find_repeat(state):
    prev_state = None
    index = 0

    states = set()

    while True:
        state = next_state(state)

        if ''.join(state) in states:
            break

        states.add(''.join(state))
        prev_state = state

        index += 1

    return state


def biodiversity_rating(state):
    index = 0
    rating = 0

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '#':
                rating += (1 << index)
            index += 1

    return rating


class TestClass:
    def test_find_repeat_0(self):
        data = [
            '....#',
            '#..#.',
            '#..##',
            '..#..',
            '#....']

        repeated_state = find_repeat(data)

        answer = [
            '.....',
            '.....',
            '.....',
            '#....',
            '.#...']

        assert repeated_state == answer

    def test_biodiversity_rating_0(self):
        data = [
            '....#',
            '#..#.',
            '#..##',
            '..#..',
            '#....']

        repeated_state = find_repeat(data)
        rating = biodiversity_rating(repeated_state)

        assert rating == 2129920


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.strip() for x in data if len(x.strip())]

    repeated_state = find_repeat(data)
    result = biodiversity_rating(repeated_state)

    print(result)
