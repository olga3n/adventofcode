#!/usr/bin/env python3

import sys


def valid_field_value(key, value):
    if key == "byr":
        return "1920" <= value <= "2002"
    if key == "iyr":
        return "2010" <= value <= "2020"
    if key == "eyr":
        return "2020" <= value <= "2030"
    if key == "hgt":
        return len(value) > 2 and (
            ("150" <= value[:-2] <= "193" and value[-2:] == "cm") or
            ("59" <= value <= "76" and value[-2:] == "in")
        )
    if key == "hcl":
        color_len = len(
            [x for x in value[1:] if x.isdigit() or 'a' <= x <= 'f']
        )
        return value[0] == "#" and color_len == 6
    if key == "ecl":
        return value in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    if key == "pid":
        return len(value) == 9


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

                if key in fields and valid_field_value(key, value):
                    passport_dict[key] = value
        else:
            if len(passport_dict.keys()) == len(fields):
                result += 1

            passport_dict = {}

    return result


class TestClass:

    def test_valid_field_values(self):
        assert valid_field_value('byr', '2002') is True
        assert valid_field_value('byr', '2003') is False

        assert valid_field_value('hgt', '60in') is True
        assert valid_field_value('hgt', '190cm') is True
        assert valid_field_value('hgt', '190in') is False
        assert valid_field_value('hgt', '190') is False

        assert valid_field_value('hcl', '#123abc') is True
        assert valid_field_value('hcl', '#123abz') is False
        assert valid_field_value('hcl', '123abc') is False

        assert valid_field_value('ecl', 'brn') is True
        assert valid_field_value('ecl', 'wat') is False

        assert valid_field_value('pid', '000000001') is True
        assert valid_field_value('pid', '0123456789') is False

    def test_invalid_passports(self):
        data = [
            'eyr:1972 cid:100',
            'hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
            '',
            'iyr:2019',
            'hcl:#602927 eyr:1967 hgt:170cm',
            'ecl:grn pid:012533040 byr:1946',
            '',
            'hcl:dab227 iyr:2012',
            'ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
            '',
            'hgt:59cm ecl:zzz',
            'eyr:2038 hcl:74454a iyr:2023',
            'pid:3556412378 byr:2007'
        ]

        assert valid_passports(data) == 0

    def test_valid_passports(self):
        data = [
            'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980',
            'hcl:#623a2f',
            '',
            'eyr:2029 ecl:blu cid:129 byr:1989',
            'iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
            '',
            'hcl:#888785',
            'hgt:164cm byr:2001 iyr:2015 cid:88',
            'pid:545766238 ecl:hzl',
            'eyr:2022',
            '',
            'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'
        ]

        assert valid_passports(data) == 4


def main():
    data = [line.strip() for line in sys.stdin]
    result = valid_passports(data)
    print(result)


if __name__ == '__main__':
    main()
