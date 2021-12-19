#!/usr/bin/env python3

import sys
from typing import List, Tuple


def parse_data(data: List[str]) -> List[List[Tuple[int, ...]]]:
    scanners_data = []
    new_scanner: List[Tuple[int, ...]] = []

    for line in data:
        if 'scanner' in line:
            if len(new_scanner):
                scanners_data.append(new_scanner)
            new_scanner = []
            continue
        if len(line) == 0:
            continue
        position = tuple(map(int, line.split(',')))
        new_scanner.append(position)

    if len(new_scanner):
        scanners_data.append(new_scanner)

    return scanners_data


def rotation(position: Tuple[int, ...], mode: int) -> Tuple[int, ...]:
    x, y, z = position

    if mode == 0:
        return (x, y, z)
    elif mode == 1:
        return (x, -y, -z)
    elif mode == 2:
        return (x, -z, y)
    elif mode == 3:
        return (x, z, -y)

    elif mode == 4:
        return (-x, z, y)
    elif mode == 5:
        return (-x, -z, -y)
    elif mode == 6:
        return (-x, y, -z)
    elif mode == 7:
        return (-x, -y, z)

    elif mode == 8:
        return (y, z, x)
    elif mode == 9:
        return (y, -z, -x)
    elif mode == 10:
        return (y, -x, z)
    elif mode == 11:
        return (y, x, -z)

    elif mode == 12:
        return (-y, x, z)
    elif mode == 13:
        return (-y, -x, -z)
    elif mode == 14:
        return (-y, -z, x)
    elif mode == 15:
        return (-y, z, -x)

    elif mode == 16:
        return (z, x, y)
    elif mode == 17:
        return (z, -x, -y)
    elif mode == 18:
        return (z, -y, x)
    elif mode == 19:
        return (z, y, -x)

    elif mode == 20:
        return (-z, y, x)
    elif mode == 21:
        return (-z, -y, -x)
    elif mode == 22:
        return (-z, -x, y)
    elif mode == 23:
        return (-z, x, -y)

    return (x, y, z)


def move(point: Tuple, shift: Tuple) -> Tuple:
    return (
        point[0] + shift[0],
        point[1] + shift[1],
        point[2] + shift[2]
    )


def find_overlap(
        scanner1: List[Tuple], scanner2: List[Tuple], min_count: int = 12
) -> Tuple[bool, List[Tuple], Tuple]:
    for point1 in scanner1:
        for mode in range(24):
            rotated_scanner = [rotation(point, mode) for point in scanner2]
            for ind in range(len(rotated_scanner) - (min_count - 1)):
                pos = rotated_scanner[ind]
                shift = (
                    point1[0] - pos[0],
                    point1[1] - pos[1],
                    point1[2] - pos[2]
                )
                shifted_scanner = [
                    move(point, shift) for point in rotated_scanner
                ]
                if len(set(shifted_scanner) & set(scanner1)) >= min_count:
                    return True, shifted_scanner, shift

    return False, scanner2, (0, 0, 0)


def max_beacons_dist(data: List[str]) -> int:
    scanners_data = parse_data(data)
    true_scanners = {0}
    prev_scanners = {0}
    scanners_pos = [(0, 0, 0) for i in range(len(scanners_data))]

    while len(true_scanners) < len(scanners_data):
        new_scanners = set()
        for s2, scanner2 in enumerate(scanners_data):
            if s2 in true_scanners or s2 in prev_scanners:
                continue
            for s1 in prev_scanners:
                status, scanner2, shift = find_overlap(
                    scanners_data[s1], scanner2
                )
                scanners_data[s2] = scanner2
                scanners_pos[s2] = move(scanners_pos[s2], shift)
                if status:
                    true_scanners.add(s2)
                    new_scanners.add(s2)
                    break
        prev_scanners = new_scanners

    max_dist = 0

    for i in range(len(scanners_pos)):
        for j in range(i + 1, len(scanners_pos)):
            dist = (
                abs(scanners_pos[i][0] - scanners_pos[j][0]) +
                abs(scanners_pos[i][1] - scanners_pos[j][1]) +
                abs(scanners_pos[i][2] - scanners_pos[j][2])
            )
            max_dist = max(max_dist, dist)

    return max_dist


class TestClass():

    def test_1(self):
        data = [
            '--- scanner 0 ---',
            '404,-588,-901',
            '528,-643,409',
            '-838,591,734',
            '390,-675,-793',
            '-537,-823,-458',
            '-485,-357,347',
            '-345,-311,381',
            '-661,-816,-575',
            '-876,649,763',
            '-618,-824,-621',
            '553,345,-567',
            '474,580,667',
            '-447,-329,318',
            '-584,868,-557',
            '544,-627,-890',
            '564,392,-477',
            '455,729,728',
            '-892,524,684',
            '-689,845,-530',
            '423,-701,434',
            '7,-33,-71',
            '630,319,-379',
            '443,580,662',
            '-789,900,-551',
            '459,-707,401',
            '',
            '--- scanner 1 ---',
            '686,422,578',
            '605,423,415',
            '515,917,-361',
            '-336,658,858',
            '95,138,22',
            '-476,619,847',
            '-340,-569,-846',
            '567,-361,727',
            '-460,603,-452',
            '669,-402,600',
            '729,430,532',
            '-500,-761,534',
            '-322,571,750',
            '-466,-666,-811',
            '-429,-592,574',
            '-355,545,-477',
            '703,-491,-529',
            '-328,-685,520',
            '413,935,-424',
            '-391,539,-444',
            '586,-435,557',
            '-364,-763,-893',
            '807,-499,-711',
            '755,-354,-619',
            '553,889,-390',
            '',
            '--- scanner 2 ---',
            '649,640,665',
            '682,-795,504',
            '-784,533,-524',
            '-644,584,-595',
            '-588,-843,648',
            '-30,6,44',
            '-674,560,763',
            '500,723,-460',
            '609,671,-379',
            '-555,-800,653',
            '-675,-892,-343',
            '697,-426,-610',
            '578,704,681',
            '493,664,-388',
            '-671,-858,530',
            '-667,343,800',
            '571,-461,-707',
            '-138,-166,112',
            '-889,563,-600',
            '646,-828,498',
            '640,759,510',
            '-630,509,768',
            '-681,-892,-333',
            '673,-379,-804',
            '-742,-814,-386',
            '577,-820,562',
            '',
            '--- scanner 3 ---',
            '-589,542,597',
            '605,-692,669',
            '-500,565,-823',
            '-660,373,557',
            '-458,-679,-417',
            '-488,449,543',
            '-626,468,-788',
            '338,-750,-386',
            '528,-832,-391',
            '562,-778,733',
            '-938,-730,414',
            '543,643,-506',
            '-524,371,-870',
            '407,773,750',
            '-104,29,83',
            '378,-903,-323',
            '-778,-728,485',
            '426,699,580',
            '-438,-605,-362',
            '-469,-447,-387',
            '509,732,623',
            '647,635,-688',
            '-868,-804,481',
            '614,-800,639',
            '595,780,-596',
            '',
            '--- scanner 4 ---',
            '727,592,562',
            '-293,-554,779',
            '441,611,-461',
            '-714,465,-776',
            '-743,427,-804',
            '-660,-479,-426',
            '832,-632,460',
            '927,-485,-438',
            '408,393,-506',
            '466,436,-512',
            '110,16,151',
            '-258,-428,682',
            '-393,719,612',
            '-211,-452,876',
            '808,-476,-593',
            '-575,615,604',
            '-485,667,467',
            '-680,325,-822',
            '-627,-443,-432',
            '872,-547,-609',
            '833,512,582',
            '807,604,487',
            '839,-516,451',
            '891,-625,532',
            '-652,-548,-490',
            '30,-46,-14',
        ]
        assert max_beacons_dist(data) == 3621


def main():
    data = [x.strip() for x in sys.stdin]
    result = max_beacons_dist(data)
    print(result)


if __name__ == '__main__':
    main()
