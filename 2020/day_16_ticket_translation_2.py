#!/usr/bin/env python3

import sys


def check_value(limits, value):
    result = False

    for name, limits_ranges in limits.items():
        for value_min, value_max in limits_ranges:
            if value_min <= value <= value_max:
                result = True
                break

    return result


def parse_limits(data):
    limits = {}

    for i, line in enumerate(data):
        if not len(line):
            continue

        if line == 'your ticket:':
            break

        name, limits_line = line.split(': ')

        limits_ranges = limits_line.split(' or ')
        limits_ranges = [
            tuple(map(int, x.split('-'))) for x in limits_ranges
        ]

        limits[name] = limits_ranges

    return limits


def parse_my_ticket(data):
    for i, line in enumerate(data):
        if line == 'your ticket:':
            return list(map(int, data[i + 1].split(',')))


def parse_correct_tickets(data, limits):
    correct_tickets = []
    status = False

    for line in data:
        if line == 'nearby tickets:':
            status = True
            continue

        if status:
            values = list(map(int, line.split(',')))
            correct_ticket = True

            for value in values:
                if not check_value(limits, value):
                    correct_ticket = False
                    break

            if correct_ticket:
                correct_tickets.append(values)

    return correct_tickets


def find_fields_order(limits, correct_tickets):
    order = [None] * len(limits)

    candidates = {}

    for name, limits_ranges in limits.items():
        candidates[name] = []

        for i in range(len(correct_tickets[0])):
            is_good_candidate = True

            for ticket in correct_tickets:
                is_good_ticket = False

                for value_min, value_max in limits_ranges:
                    if value_min <= ticket[i] <= value_max:
                        is_good_ticket = True

                if not is_good_ticket:
                    is_good_candidate = False

            if is_good_candidate:
                candidates[name].append(i)

    while len(candidates):
        for name, options in candidates.items():
            if len(options) == 1:
                order[options[0]] = name
                break

        new_candidates = {}

        for name, options in candidates.items():
            new_options = [x for x in options if order[x] is None]

            if len(new_options):
                new_candidates[name] = new_options

        candidates = new_candidates

    return order


def ticket_fields(data):

    limits = parse_limits(data)
    my_ticket = parse_my_ticket(data)

    correct_tickets = parse_correct_tickets(data, limits)
    correct_tickets.append(my_ticket)

    fields_order = find_fields_order(limits, correct_tickets)

    return {x[0]: x[1] for x in zip(fields_order, my_ticket)}


def ticket_score(data):
    result = 1

    fields = ticket_fields(data)

    for name, value in fields.items():
        if name.startswith('departure'):
            result *= value

    return result


class TestClass():

    def test_ticket_fields(self):
        data = [
            'class: 0-1 or 4-19',
            'row: 0-5 or 8-19',
            'seat: 0-13 or 16-19',
            '',
            'your ticket:',
            '11,12,13',
            '',
            'nearby tickets:',
            '3,9,18',
            '15,1,5',
            '5,14,9',
        ]

        assert ticket_fields(data) == {'class': 12, 'row': 11, 'seat': 13}


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = ticket_score(data)
    print(result)


if __name__ == '__main__':
    main()
