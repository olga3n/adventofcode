#!/usr/bin/env python3

import sys


def valid_passports(data):
    fields = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid"
    }

    result = 0
    passport_dict = {}

    data.append('')

    for line in data:
        if len(line):
            for item in line.split(" "):
                key, value = item.split(":")

                if key in fields:
                    passport_dict[key] = value
        else:
            if len(passport_dict.keys()) == len(fields):
                result += 1

            passport_dict = {}

    return result


class TestClass:

    def test_1(self):
        data = [
            'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
            'byr:1937 iyr:2017 cid:147 hgt:183cm',
            '',
            'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
            'hcl:#cfa07d byr:1929',
            '',
            'hcl:#ae17e1 iyr:2013',
            'eyr:2024',
            'ecl:brn pid:760753108 byr:1931',
            'hgt:179cm',
            '',
            'hcl:#cfa07d eyr:2025 pid:166559648',
            'iyr:2011 ecl:brn hgt:59in'
        ]

        assert valid_passports(data) == 2


def main():
    data = [line.strip() for line in sys.stdin]
    result = valid_passports(data)
    print(result)


if __name__ == '__main__':
    main()
