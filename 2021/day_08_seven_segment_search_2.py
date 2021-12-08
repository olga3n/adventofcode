#!/usr/bin/env python3

import sys
from typing import List


def decode_entry(entry: str) -> int:
    result = ''
    left, right = map(lambda x: x.split(), entry.split(' | '))

    codes = left + right
    store = {i: set() for i in range(2, 8)}

    for code in codes:
        store[len(code)].add(''.join(sorted(code)))

    digit_code = {}

    digit_code[1] = next(iter(store[2]))
    digit_code[7] = next(iter(store[3]))
    digit_code[4] = next(iter(store[4]))
    digit_code[8] = next(iter(store[7]))

    digit_code[9] = [
        x for x in store[6]
        if len(set(x).intersection(set(digit_code[4]))) == 4
    ][0]

    digit_code[3] = [
        x for x in store[5]
        if len(set(x).intersection(set(digit_code[1]))) == 2
    ][0]

    digit_code[6] = [
        x for x in store[6]
        if len(set(x).intersection(set(digit_code[1]))) != 2
    ][0]

    digit_code[2] = [
        x for x in store[5]
        if len(set(x).intersection(set(digit_code[4]))) == 2
    ][0]

    digit_code[0] = [
        x for x in store[6]
        if x != digit_code[9] and x != digit_code[6]
    ][0]

    digit_code[5] = [
        x for x in store[5]
        if x != digit_code[3] and x != digit_code[2]
    ][0]

    digit_code_inv = {v: k for k, v in digit_code.items()}

    for code in right:
        result += str(digit_code_inv[''.join(sorted(code))])

    return int(result)


def decode_sum(data: List[str]) -> int:
    return sum([decode_entry(entry) for entry in data])


class TestClass():

    def test_1(self):
        data = [
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
            'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
            'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
            'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
            'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
            'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
            'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
            'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
            'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
        ]

        assert decode_entry(data[0]) == 8394
        assert decode_entry(data[1]) == 9781
        assert decode_entry(data[2]) == 1197
        assert decode_entry(data[3]) == 9361
        assert decode_entry(data[4]) == 4873
        assert decode_entry(data[5]) == 8418
        assert decode_entry(data[6]) == 4548
        assert decode_entry(data[7]) == 1625
        assert decode_entry(data[8]) == 8717
        assert decode_entry(data[9]) == 4315

    def test_2(self):
        data = [
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
            'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
            'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
            'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
            'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
            'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
            'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
            'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
            'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
        ]

        assert decode_sum(data) == 61229


def main():
    data = [x.strip() for x in sys.stdin]
    result = decode_sum(data)
    print(result)


if __name__ == '__main__':
    main()
