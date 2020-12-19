#!/usr/bin/env python3

import sys


class State:

    def __init__(self, seq, msg_index):
        self.seq = seq
        self.msg_index = msg_index


def is_valid_msg(grammar, msg):
    result = False

    state = State(['0'], 0)
    states = [state]

    while True:
        if not len(states):
            break

        state = states.pop()

        if not len(state.seq) or state.msg_index >= len(msg):
            break

        if grammar[state.seq[0]][0][0] in {'a', 'b'}:
            if msg[state.msg_index] != grammar[state.seq[0]][0][0]:
                continue
            else:
                if state.msg_index == len(msg) - 1 and len(state.seq) == 1:
                    result = True
                    break
                elif len(state.seq) > 1:
                    new_state = State(state.seq[1:], state.msg_index + 1)
                    states.append(new_state)
        else:
            for option in grammar[state.seq[0]]:
                new_state = State(option + state.seq[1:], state.msg_index)
                states.append(new_state)

    return result


def valid_messages(data):
    grammar = {}
    messages = []

    for line in data:
        if not len(line):
            continue

        if line[0].isdigit():
            rule_num, rule_out = line.split(': ')
            outputs = [x.split(' ') for x in rule_out.split(' | ')]

            for i in range(len(outputs)):
                for j in range(len(outputs[i])):
                    if outputs[i][j][0] == '"':
                        outputs[i][j] = outputs[i][j][1:-1]

            grammar[rule_num] = outputs
        else:
            messages.append(line)

    return len([1 for x in messages if is_valid_msg(grammar, x)])


class TestClass():

    def test_valid_messages(self):

        data = [
            '0: 4 1 5',
            '1: 2 3 | 3 2',
            '2: 4 4 | 5 5',
            '3: 4 5 | 5 4',
            '4: "a"',
            '5: "b"',
            '',
            'ababbb',
            'bababa',
            'abbbab',
            'aaabbb',
            'aaaabbb'
        ]

        assert valid_messages(data) == 2


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = valid_messages(data)
    print(result)


if __name__ == '__main__':
    main()
