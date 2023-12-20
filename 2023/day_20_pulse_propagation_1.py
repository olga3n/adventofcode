#!/usr/bin/env

import sys
from typing import Iterable, Set, Optional, Dict
from dataclasses import dataclass
from collections import deque


@dataclass
class ModuleB:
    recievers: Set[str]

    def process_pulse(self, pulse: bool, input_name: str):
        for reciever in self.recievers:
            yield (reciever, pulse)


@dataclass
class ModuleF(ModuleB):
    is_on: bool = False

    def process_pulse(self, pulse: bool, input_name: str):
        if not pulse:
            self.is_on = not self.is_on
            for reciever in self.recievers:
                yield (reciever, self.is_on)


@dataclass
class ModuleC(ModuleB):
    statuses: Optional[Dict[str, bool]] = None

    def save_inputs(self, inputs: Iterable[str]):
        self.statuses = {}
        for name in inputs:
            self.statuses[name] = False

    def process_pulse(self, pulse: bool, input_name: str):
        self.statuses[input_name] = pulse
        pulse = not all(self.statuses.values())
        yield from super().process_pulse(pulse, input_name)


def build_modules(data: Iterable[str]) -> Dict[str, ModuleB]:
    modules = {}
    conjs = []

    for line in data:
        m_in, m_out = line.split(' -> ')
        m_out = m_out.split(', ')

        if m_in == 'broadcaster':
            modules[m_in] = ModuleB(m_out)
        elif m_in.startswith('%'):
            modules[m_in[1:]] = ModuleF(m_out)
        elif m_in.startswith('&'):
            modules[m_in[1:]] = ModuleC(m_out)
            conjs.append(m_in[1:])

    for name_out in conjs:
        inputs = set()
        for name_in, module in modules.items():
            if name_out in module.recievers:
                inputs.add(name_in)
        modules[name_out].save_inputs(list(inputs))

    return modules


def pulses_score(data: Iterable[str], cnt: int = 1000) -> int:
    modules = build_modules(data)
    pulses = {False: 0, True: 0}

    for _ in range(cnt):
        queue = deque([('broadcaster', False, '')])
        while queue:
            name, pulse, prev_name = queue.popleft()
            pulses[pulse] += 1
            if name not in modules:
                continue
            new_items = modules[name].process_pulse(pulse, prev_name)
            for new_name, new_pulse in new_items:
                queue.append((new_name, new_pulse, name))

    return pulses[True] * pulses[False]


def test_pulses_score_1():
    data = [
        'broadcaster -> a, b, c',
        '%a -> b',
        '%b -> c',
        '%c -> inv',
        '&inv -> a',
    ]
    assert pulses_score(data) == 32000000


def test_pulses_score_2():
    data = [
        'broadcaster -> a',
        '%a -> inv, con',
        '&inv -> b',
        '%b -> con',
        '&con -> output',
    ]
    assert pulses_score(data) == 11687500


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = pulses_score(data)
    print(result)


if __name__ == '__main__':
    main()
