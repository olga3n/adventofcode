#!/usr/bin/env python3

import sys
import re
import logging
from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Dict, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('main')


@dataclass(frozen=True)
class State:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    minute: int = 0

    @classmethod
    def from_string(cls, line):
        cost = {}
        for material in line.split(' and '):
            size, name = material.split()
            cost[name] = int(size)
        return cls(**cost)


def parse_blueprints(data: Iterable[str]) -> List[Dict[str, State]]:
    blueprints = []

    for line in data:
        if line.startswith('Blueprint'):
            costs = re.findall(r'robot costs ([^\.]+)\.', line)
            blueprint = {
                'ore': State.from_string(costs[0]),
                'clay': State.from_string(costs[1]),
                'obsidian': State.from_string(costs[2]),
                'geode': State.from_string(costs[3])
            }
            blueprints.append(blueprint)

    return blueprints


def can_buy(materials: State, robot: State) -> bool:
    return (
        materials.ore >= robot.ore and
        materials.clay >= robot.clay and
        materials.obsidian >= robot.obsidian and
        materials.geode >= robot.geode
    )


def buy_robot(
    robots: State, materials: State, robot: State, robot_type: str
) -> Tuple[State, State]:
    new_robots = State(
        ore=robots.ore + int(robot_type == 'ore'),
        clay=robots.clay + int(robot_type == 'clay'),
        obsidian=robots.obsidian + int(robot_type == 'obsidian'),
        geode=robots.geode + int(robot_type == 'geode'),
        minute=robots.minute + 1
    )
    new_materials = State(
        ore=materials.ore - robot.ore,
        clay=materials.clay - robot.clay,
        obsidian=materials.obsidian - robot.obsidian,
        geode=materials.geode - robot.geode,
    )
    return new_robots, new_materials


def max_geodes(blueprint: Dict[str, State], minutes: int = 32) -> int:
    queue = deque([
        (State(ore=2, minute=blueprint['ore'].ore + 1), State(ore=1))
    ])

    visited = set()
    result = 0

    max_ore = max(
        blueprint['ore'].ore,
        blueprint['clay'].ore,
        blueprint['obsidian'].ore,
        blueprint['geode'].ore
    )

    max_clay = max(
        blueprint['ore'].clay,
        blueprint['clay'].clay,
        blueprint['obsidian'].clay,
        blueprint['geode'].clay
    )

    sum_ore = sum((
        blueprint['ore'].ore,
        blueprint['clay'].ore,
        blueprint['obsidian'].ore,
        blueprint['geode'].ore
    ))

    last_minute = 0

    while queue:
        robots, materials = queue.popleft()

        key = (robots, materials)

        if key in visited:
            continue

        visited.add(key)

        if robots.minute > last_minute:
            logger.info('%s/%s', robots.minute + 1, minutes)
            to_remove = []
            for item in visited:
                if item[0].minute == last_minute:
                    to_remove.append(item)
            for item in to_remove:
                visited.remove(item)
            last_minute = robots.minute

        if robots.obsidian == 0 and robots.minute + 4 > minutes:
            continue

        if robots.clay == 0 and robots.minute + 6 > minutes:
            continue

        for robot_type in ('geode', 'obsidian', 'clay', 'ore', ''):
            if robot_type in blueprint and robots.minute + 1 < minutes:

                if robot_type == 'obsidian' and robots.minute + 4 > minutes:
                    continue

                if robot_type == 'clay':
                    if robots.clay >= max_clay or robots.minute + 6 > minutes:
                        continue

                if robot_type == 'ore':
                    if robots.ore >= max_ore or robots.minute + 4 > minutes:
                        continue

                if can_buy(materials, blueprint[robot_type]):
                    new_robots, new_materials = buy_robot(
                        robots, materials, blueprint[robot_type], robot_type
                    )
                else:
                    continue
            else:
                new_robots = State(
                    ore=robots.ore,
                    clay=robots.clay,
                    obsidian=robots.obsidian,
                    geode=robots.geode,
                    minute=robots.minute + 1
                )
                new_materials = materials

            new_materials = State(
                ore=new_materials.ore + robots.ore,
                clay=new_materials.clay + robots.clay,
                obsidian=new_materials.obsidian + robots.obsidian,
                geode=new_materials.geode + robots.geode
            )

            if new_robots.minute == minutes:
                if new_materials.geode:
                    result = max(new_materials.geode, result)
                continue

            if (new_robots, new_materials) in visited:
                continue

            queue.append((new_robots, new_materials))

            if robot_type == 'geode':
                break

            if robots.ore == max_ore:
                break

            if robot_type == 'obsidian':
                if new_materials.ore >= sum_ore - blueprint['obsidian'].ore:
                    break

            if robot_type == 'clay':
                if new_materials.ore >= sum_ore - blueprint['clay'].ore:
                    break

            if robot_type == 'ore':
                if new_materials.ore >= sum_ore - blueprint['ore'].ore:
                    break

    return result


def blueprints_score(data: Iterable[str], take_n: int = 3) -> int:
    blueprints = parse_blueprints(data)
    result = 1
    for index, blueprint in enumerate(blueprints):
        logger.info('Blueprint %s', index + 1)
        score = max_geodes(blueprint)
        logger.info('Blueprint %s: %s', index + 1, score)
        result *= score
        if index == take_n - 1:
            break
    return result


def test_max_geodes():
    data = [
        'Blueprint 1:' +
        '  Each ore robot costs 4 ore.' +
        '  Each clay robot costs 2 ore.' +
        '  Each obsidian robot costs 3 ore and 14 clay.' +
        '  Each geode robot costs 2 ore and 7 obsidian.',
        'Blueprint 2:' +
        '  Each ore robot costs 2 ore.' +
        '  Each clay robot costs 3 ore.' +
        '  Each obsidian robot costs 3 ore and 8 clay.' +
        '  Each geode robot costs 3 ore and 12 obsidian.'
    ]

    blueprints = parse_blueprints(data)

    assert max_geodes(blueprints[0]) == 56
    assert max_geodes(blueprints[1]) == 62


def main():
    data = sys.stdin
    result = blueprints_score(data)
    print(result)


if __name__ == '__main__':
    main()
