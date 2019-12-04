#!/usr/bin/env python3

import argparse


def calc_passwords_in_range_rec(a, b, prefix, tail_len):

    if tail_len == 0:
        if len(set(prefix)) < len(prefix):
            freq = {}

            for c in prefix:
                if c not in freq:
                    freq[c] = 1
                else:
                    freq[c] += 1

            return 1 if 2 in freq.values() else 0
        else:
            return 0

    result = 0

    first_n = 0 if not len(prefix) else int(prefix[-1])

    for n_i in range(first_n, 10):
        new_prefix = prefix + str(n_i)

        if a[:len(new_prefix)] <= new_prefix <= b[:len(new_prefix)]:
            result += calc_passwords_in_range_rec(
                    a, b, new_prefix, tail_len - 1)

    return result


def calc_passwords_in_range(a, b):
    return calc_passwords_in_range_rec(a, b, '', 6)


class TestClass():
    def test_calc_passwords_in_range_1(self):
        a = '112233'
        b = '112233'

        assert calc_passwords_in_range(a, b) == 1

    def test_calc_passwords_in_range_2(self):
        a = '123444'
        b = '123444'

        assert calc_passwords_in_range(a, b) == 0

    def test_calc_passwords_in_range_3(self):
        a = '111122'
        b = '111122'

        assert calc_passwords_in_range(a, b) == 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', help='min value', default='245318')
    parser.add_argument('-b', help='max value', default='765747')

    args = parser.parse_args()

    result = calc_passwords_in_range(args.a, args.b)

    print(result)
