#!/usr/bin/env python3

import sys


def expand_state(state):

    new_cubes = []

    for cube in state:
        new_frames = []

        for frame in cube:
            new_lines = []

            for line in frame:
                new_lines.append('.' + line + '.')

            empty_line = '.' * (len(line) + 2)
            new_frames.append([empty_line] + new_lines + [empty_line])

        empty_frame = [empty_line] * (len(frame) + 2)
        new_cubes.append([empty_frame] + new_frames + [empty_frame])

    empty_cube = [empty_frame] * (len(cube) + 2)
    new_state = [empty_cube] + new_cubes + [empty_cube]

    return new_state


def calc_active_cubes(state, i, j, k, t):
    result = 0

    for ii in [-1, 0, 1]:
        for jj in [-1, 0, 1]:
            for kk in [-1, 0, 1]:
                for tt in [-1, 0, 1]:

                    if ii == 0 and jj == 0 and kk == 0 and tt == 0:
                        continue

                    if i + ii >= len(state) or i + ii < 0:
                        continue

                    if j + jj >= len(state[i + ii]) or j + jj < 0:
                        continue

                    if k + kk >= len(state[i + ii][j + jj]) or k + kk < 0:
                        continue

                    if (t + tt >= len(state[i + ii][j + jj][k + kk]) or
                            t + tt < 0):
                        continue

                    if state[i + ii][j + jj][k + kk][t + tt] == '#':
                        result += 1

    return result


def cycle_cubes(data, cycle_count=6):
    state = [[data]]

    for cycle in range(cycle_count):
        state = expand_state(state)

        new_state = []

        for i in range(len(state)):
            new_cube = []

            for j in range(len(state[i])):
                new_frame = []

                for k in range(len(state[i][j])):
                    new_line = []

                    for t in range(len(state[i][j][k])):
                        active = calc_active_cubes(state, i, j, k, t)

                        if state[i][j][k][t] == '#':
                            if 2 <= active <= 3:
                                new_line.append('#')
                            else:
                                new_line.append('.')
                        else:
                            if active == 3:
                                new_line.append('#')
                            else:
                                new_line.append('.')

                    new_frame.append(''.join(new_line))

                new_cube.append(new_frame)

            new_state.append(new_cube)

        state = new_state

    result = 0

    for cube in state:
        for frame in cube:
            for line in frame:
                result += len([1 for x in line if x == '#'])

    return result


class TestClass():

    def test_cycle_cubes(self):
        data = [
            '.#.',
            '..#',
            '###'
        ]

        assert cycle_cubes(data) == 848


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = cycle_cubes(data)
    print(result)


if __name__ == '__main__':
    main()
