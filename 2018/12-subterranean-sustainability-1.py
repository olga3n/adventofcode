#!/usr/bin/env python3

import sys

import unittest
import textwrap


def parse_data(data):
    current_state = data[0].split(": ")[1]

    rules = {}

    for item in data[1:]:
        pattern, result = item.split(" => ")
        rules[pattern] = result

    return rules, current_state


def generation(current_state, rules, N=20):
    first_ind = 0

    for i in range(N):

        state = ''

        if current_state[0] == '#':
            first_ind -= 2
            current_state = '....' + current_state
        elif current_state[1] == '#':
            first_ind -= 1
            current_state = '...' + current_state
        elif current_state[2] == '#':
            current_state = '..' + current_state
        elif current_state[3] == '#':
            first_ind += 1
            current_state = '.' + current_state
        else:
            first_ind += 2

        if current_state[-1] == "#":
            current_state += '....'
        elif current_state[-2] == '#':
            current_state += '...'
        elif current_state[-3] == '#':
            current_state += '..'
        elif current_state[-4] == '#':
            current_state += '.'

        for j in range(len(current_state) - 4):
            pattern = current_state[j: j + 5]

            if pattern in rules:
                state += rules[pattern]
            else:
                state += '.'

        current_state = state

    return state, first_ind


def process(data, N=20):
    rules, current_state = parse_data(data)

    state, first_ind = generation(current_state, rules, N=N)

    result = 0

    for ind, ch in enumerate(state):
        if ch == '#':
            result += ind + first_ind

    return result


class TestStringMethods(unittest.TestCase):

    def test_0(self):

        data = textwrap.dedent("""\
            initial state: #..#.#..##......###...###

            ...## => #
            ..#.. => #
            .#... => #
            .#.#. => #
            .#.## => #
            .##.. => #
            .#### => #
            #.#.# => #
            #.### => #
            ##.#. => #
            ##.## => #
            ###.. => #
            ###.# => #
            ####. => #
        """).split("\n")

        data = [x for x in data if len(x)]

        self.assertEqual(process(data, N=20), 325)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = process(data)

    print(v)
