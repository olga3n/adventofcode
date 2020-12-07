#!/usr/bin/env python3

import sys


def valid_bag_colors(rules, bag_color='shiny gold'):
    result = 0

    rules_dict = {}
    color_stat = {}

    for line in rules:
        color, content = line.split(' bags contain ')
        rules_dict[color] = {}

        if content != 'no other bags.':
            for bag_type in content.split(', '):
                prs = bag_type.split(' ')
                rules_dict[color][prs[1] + ' ' + prs[2]] = int(prs[0])
        else:
            color_stat[color] = 0

    color_stat[bag_color] = 1

    reverse_rules_dict = {}

    for color_1, content in rules_dict.items():
        for color_2, count in content.items():
            if color_2 not in reverse_rules_dict:
                reverse_rules_dict[color_2] = [color_1]
            else:
                reverse_rules_dict[color_2].append(color_1)

    candidates = []

    for item in color_stat:
        if item in reverse_rules_dict:
            for color in reverse_rules_dict[item]:
                if color not in color_stat:
                    candidates.append(color)

    while len(candidates):
        new_candidates = []

        for candidate in candidates:
            candidate_stat = 0
            known_colors = 0

            for color, count in rules_dict[candidate].items():
                if color == bag_color:
                    candidate_stat += count
                    known_colors += 1
                elif color in color_stat:
                    candidate_stat += color_stat[color]
                    known_colors += 1

            if len(rules_dict[candidate]) == known_colors:
                color_stat[candidate] = candidate_stat

                if candidate in reverse_rules_dict:
                    for color in reverse_rules_dict[candidate]:
                        if color not in color_stat:
                            candidates.append(color)
            else:
                new_candidates.append(candidate)

        candidates = new_candidates

    result = len([
        color for color, count in color_stat.items()
        if count and color != bag_color
    ])

    return result


class TestClass:

    def test_valid_bag_colors(self):
        data = [
            'light red bags contain 1 bright white bag, 2 muted yellow bags.',
            'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
            'bright white bags contain 1 shiny gold bag.',
            'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
            'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
            'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
            'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
            'faded blue bags contain no other bags.',
            'dotted black bags contain no other bags.'
        ]

        assert valid_bag_colors(data) == 4


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = valid_bag_colors(data)
    print(result)


if __name__ == '__main__':
    main()
