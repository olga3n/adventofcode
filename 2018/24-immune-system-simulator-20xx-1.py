#!/usr/bin/env python3

import sys
import re

import logging

import unittest
import textwrap


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_data(data):
    imm_flag = False
    inf_flag = False

    imm_cnt = 0
    inf_cnt = 0

    units_dict = {}
    hit_points_dict = {}
    damage_dict = {}
    damage_type_dict = {}
    initiative_dict = {}

    immune_dict = {}
    weak_dict = {}

    group_re = re.compile(
        r"""(\d+) units each with (\d+) hit points (.*)"""
        r"""with an attack that does (\d+) (\w+) damage """
        r"""at initiative (\d+)""")

    for line in data:
        if 'Immune System' in line:
            imm_flag = True
            inf_flag = False

        elif 'Infection' in line:
            inf_flag = True
            imm_flag = False

        elif len(line):
            m = re.match(group_re, line)

            if m:
                if imm_flag:
                    group_id = 'imm_' + str(imm_cnt)
                    imm_cnt += 1

                elif inf_flag:
                    group_id = 'inf_' + str(inf_cnt)
                    inf_cnt += 1

                units, hit_points, condition, \
                    damage, damage_type, initiative = m.groups()

                units_dict[group_id] = int(units)
                hit_points_dict[group_id] = int(hit_points)
                damage_dict[group_id] = int(damage)
                damage_type_dict[group_id] = damage_type
                initiative_dict[group_id] = int(initiative)

                if len(condition):
                    prs = re.split(r'[\(\);]\s?', condition)

                    for item in prs:
                        if len(item):
                            if 'immune to' in item:
                                lst = item[len('immune to '):].split(', ')
                                immune_dict[group_id] = lst

                            elif 'weak to' in item:
                                lst = item[len('weak to '):].split(', ')
                                weak_dict[group_id] = lst

                if group_id not in immune_dict:
                    immune_dict[group_id] = []

                if group_id not in weak_dict:
                    weak_dict[group_id] = []
    return \
        units_dict, \
        hit_points_dict, \
        damage_dict, \
        damage_type_dict, \
        initiative_dict, \
        immune_dict, \
        weak_dict


def combat_score(data):

    units_dict, hit_points_dict, \
        damage_dict, damage_type_dict, initiative_dict, \
        immune_dict, weak_dict = parse_data(data)

    while True:
        imm_groups = [
            group_id for group_id in units_dict.keys()
            if units_dict[group_id] > 0 and 'imm' in group_id]

        inf_groups = [
            group_id for group_id in units_dict.keys()
            if units_dict[group_id] > 0 and 'inf' in group_id]

        if len(imm_groups) == 0 or len(inf_groups) == 0:
            break

        effective_power_dict = {}

        for group_id in units_dict.keys():
            effective_power_dict[group_id] = \
                (units_dict[group_id] * damage_dict[group_id],
                    initiative_dict[group_id])

        groups = sorted(
            effective_power_dict.items(),
            key=lambda x: x[1], reverse=True)

        logging.info("groups: %s" % groups)
        logging.info("units: %s" % units_dict)

        target_selection = {}
        attacks = {}

        for item in groups:
            group_id = item[0]

            if 'imm' in group_id:
                targets = inf_groups

            elif 'inf' in group_id:
                targets = imm_groups

            target_pr = []

            for target in targets:
                if target not in target_selection:
                    target_damage = effective_power_dict[group_id][0]

                    if damage_type_dict[group_id] in immune_dict[target]:
                        target_damage = 0

                    if damage_type_dict[group_id] in weak_dict[target]:
                        target_damage *= 2

                    target_pr.append((
                        target_damage,
                        effective_power_dict[target][0],
                        initiative_dict[target],
                        target))

            if len(target_pr) and units_dict[group_id] > 0:
                target_info = sorted(target_pr, reverse=True)[0]

                if target_info[0] > 0:

                    attacks[(initiative_dict[group_id], group_id)] = \
                        (target_info[-1], target_info[0])

                    target_selection[target_info[-1]] = target_info[0]

        for attack_key in sorted(attacks.keys(), reverse=True):

            attack_id = attack_key[1]

            if units_dict[attack_id] < 1:
                continue

            target, target_damage_prev = attacks[attack_key]

            effective_power_dict[attack_id] = \
                (units_dict[attack_id] * damage_dict[attack_id],
                    initiative_dict[attack_id])

            target_damage = effective_power_dict[attack_id][0]

            if damage_type_dict[attack_id] in immune_dict[target]:
                target_damage = 0

            if damage_type_dict[attack_id] in weak_dict[target]:
                target_damage *= 2

            killed_units = target_damage // hit_points_dict[target]
            killed_units = min(units_dict[target], killed_units)

            units_dict[target] -= killed_units

            logging.info(
                "%s -> %s, damage: %s, killed: %s" %
                (attack_id, target, target_damage, killed_units))

    result = sum(units_dict.values())

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            Immune System:
            17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
            989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

            Infection:
            801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
            4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
            """).rstrip().split("\n")

        self.assertEqual(combat_score(data), 5216)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]

    v = combat_score(data)

    print(v)
