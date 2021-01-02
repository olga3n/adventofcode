#!/usr/bin/env python3

import sys


class Node():

    def __init__(self, value):
        self.value = value
        self.next = None


def game_cups(data, moves=100):

    data = [int(x) for x in data]

    node_dict = {}

    curr_node = Node(data[-1])
    node_dict[data[-1]] = curr_node

    for i in range(len(data) - 2, -1, -1):
        new_node = Node(data[i])
        new_node.next = curr_node

        node_dict[data[i]] = new_node
        curr_node = new_node

    node_dict[data[-1]].next = curr_node

    for i in range(moves):

        picked = [
            curr_node.next,
            curr_node.next.next,
            curr_node.next.next.next
        ]

        curr_node.next = curr_node.next.next.next.next

        picked_values = {x.value for x in picked}

        value = curr_node.value - 1

        while True:
            if value <= 0:
                value = max(data)

            if value not in picked_values:
                dest = node_dict[value]
                break

            value = value - 1

        tmp = dest.next
        dest.next = picked[0]
        picked[-1].next = tmp

        curr_node = curr_node.next

    curr_node = node_dict[1]
    result = ''

    while len(result) < len(data) - 1:
        curr_node = curr_node.next
        result += str(curr_node.value)

    return result


class TestClass():

    def test_game_cups(self):
        assert game_cups('389125467', moves=10) == '92658374'
        assert game_cups('389125467', moves=100) == '67384529'


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = game_cups(data[0], moves=100)
    print(result)


if __name__ == '__main__':
    main()
