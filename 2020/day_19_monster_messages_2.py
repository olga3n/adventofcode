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

    grammar['8'] = [['42'], ['42', '8']]
    grammar['11'] = [['42', '31'], ['42', '11', '31']]

    return len([1 for x in messages if is_valid_msg(grammar, x)])


class TestClass():

    def test_valid_messages(self):

        data = [
            '42: 9 14 | 10 1',
            '9: 14 27 | 1 26',
            '10: 23 14 | 28 1',
            '1: "a"',
            '11: 42 31',
            '5: 1 14 | 15 1',
            '19: 14 1 | 14 14',
            '12: 24 14 | 19 1',
            '16: 15 1 | 14 14',
            '31: 14 17 | 1 13',
            '6: 14 14 | 1 14',
            '2: 1 24 | 14 4',
            '0: 8 11',
            '13: 14 3 | 1 12',
            '15: 1 | 14',
            '17: 14 2 | 1 7',
            '23: 25 1 | 22 14',
            '28: 16 1',
            '4: 1 1',
            '20: 14 14 | 1 15',
            '3: 5 14 | 16 1',
            '27: 1 6 | 14 18',
            '14: "b"',
            '21: 14 1 | 1 14',
            '25: 1 1 | 1 14',
            '22: 14 14',
            '8: 42',
            '26: 14 22 | 1 20',
            '18: 15 15',
            '7: 14 5 | 1 21',
            '24: 14 1',
            '',
            'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
            'bbabbbbaabaabba',
            'babbbbaabbbbbabbbbbbaabaaabaaa',
            'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
            'bbbbbbbaaaabbbbaaabbabaaa',
            'bbbababbbbaaaaaaaabbababaaababaabab',
            'ababaaaaaabaaab',
            'ababaaaaabbbaba',
            'baabbaaaabbaaaababbaababb',
            'abbbbabbbbaaaababbbbbbaaaababb',
            'aaaaabbaabaaaaababaa',
            'aaaabbaaaabbaaa',
            'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
            'babaaabbbaaabaababbaabababaaab',
            'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'
        ]

        assert valid_messages(data) == 12


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = valid_messages(data)
    print(result)


if __name__ == '__main__':
    main()
