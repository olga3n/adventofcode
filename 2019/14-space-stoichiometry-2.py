#!/usr/bin/env python3

import sys
import re


def produce_fuel(reactions, coeff):
    amount = 0

    state_in = dict(reactions['FUEL'][0])

    for k in state_in.keys():
        state_in[k] *= coeff

    state_extra = {}

    while len(state_in):
        k_i = list(state_in.keys())[0]
        v_i = state_in[k_i]

        if k_i == 'ORE':
            amount += v_i
        else:
            left, right = reactions[k_i]
            v_j = right[k_i]

            coeff = 1 if v_j >= v_i else (v_i + v_j - 1) // v_j
            extra_v_i = v_j * coeff - v_i

            for k, v in left.items():
                if k in state_extra:
                    if state_extra[k] > v * coeff:
                        state_extra[k] -= v * coeff
                    else:
                        if state_extra[k] != v * coeff:
                            if k not in state_in:
                                state_in[k] = 0

                            state_in[k] += v * coeff - state_extra[k]

                        del state_extra[k]
                else:
                    if k not in state_in:
                        state_in[k] = 0

                    state_in[k] += v * coeff

            if extra_v_i:
                state_extra[k_i] = extra_v_i

        del state_in[k_i]

    return amount


def max_fuel(reactions, ore):
    fuel = 0

    a = ore // produce_fuel(reactions, 1)
    b = a * 2

    while b - a > 1:
        amount = produce_fuel(reactions, (a + b) // 2)

        if amount > ore:
            b = (a + b) // 2 - 1
        else:
            a = (a + b) // 2

    fuel = b if produce_fuel(reactions, b) < ore else a

    return fuel


def parse_input(data):
    reactions = {}

    for line in data:
        line = line.strip()
        if line:
            m = re.match(r'(.+) => (.+)', line)
            if m:
                left, right = m.groups()

                left = [x.split(' ') for x in left.split(', ')]
                left = {x[1]: int(x[0]) for x in left}

                right = right.split(' ')
                chemical = right[1]

                right = {right[1]: int(right[0])}

                reactions[chemical] = (left, right)

    return reactions


class TestClass:
    def test_minimun_amount_of_ORE_0(self):
        data = [
            '157 ORE => 5 NZVS',
            '165 ORE => 6 DCFZ',
            '44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
            '12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ',
            '179 ORE => 7 PSHF',
            '177 ORE => 5 HKGWZ',
            '7 DCFZ, 7 PSHF => 2 XJWVT',
            '165 ORE => 2 GPVTF',
            '3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT']

        reactions = parse_input(data)
        ore = 1000000000000

        result = max_fuel(reactions, ore)

        assert result == 82892753

    def test_minimun_amount_of_ORE_1(self):
        data = [
            '2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG',
            '17 NVRVD, 3 JNWZP => 8 VPVL',
            '53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL',
            '22 VJHF, 37 MNCFX => 5 FWMGM',
            '139 ORE => 4 NVRVD',
            '144 ORE => 7 JNWZP',
            '5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC',
            '5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV',
            '145 ORE => 6 MNCFX',
            '1 NVRVD => 8 CXFTF',
            '1 VJHF, 6 MNCFX => 4 RFSQX',
            '176 ORE => 6 VJHF']

        reactions = parse_input(data)
        ore = 1000000000000

        result = max_fuel(reactions, ore)

        assert result == 5586022

    def test_minimun_amount_of_ORE_2(self):
        data = [
            '171 ORE => 8 CNZTR',
            '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => '
            '4 PLWSL',
            '114 ORE => 4 BHXH',
            '14 VRPVC => 6 BMBT',
            '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
            '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => '
            '6 FHTLT',
            '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
            '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
            '5 BMBT => 4 WPTQ',
            '189 ORE => 9 KTJDG',
            '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
            '12 VRPVC, 27 CNZTR => 2 XDBXC',
            '15 KTJDG, 12 BHXH => 5 XCVML',
            '3 BHXH, 2 VRPVC => 7 MZWV',
            '121 ORE => 7 VRPVC',
            '7 XCVML => 6 RJRHP',
            '5 BHXH, 4 VRPVC => 5 LTCX']

        reactions = parse_input(data)
        ore = 1000000000000

        result = max_fuel(reactions, ore)

        assert result == 460664


if __name__ == '__main__':
    data = sys.stdin.readlines()

    reactions = parse_input(data)
    ore = 1000000000000

    result = max_fuel(reactions, ore)

    print(result)
