#!/usr/bin/env python3

import sys


class Node():

    def __init__(self, value):
        self.value = value
        self.next = None


def star_cups(data, moves=10000000, max_value=1000000):

    data = [int(x) for x in data]
    data += list(range(max(data) + 1, max_value + 1))

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
                value = max_value

            if value not in picked_values:
                dest = node_dict[value]
                break

            value = value - 1

        tmp = dest.next
        dest.next = picked[0]
        picked[-1].next = tmp

        curr_node = curr_node.next

    return node_dict[1].next.value * node_dict[1].next.next.value


class TestClass():

    def test_star_cups(self):
        assert star_cups('389125467', moves=10000000) == 149245887792


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = star_cups(data[0], moves=10000000)
    print(result)


if __name__ == '__main__':
    main()
