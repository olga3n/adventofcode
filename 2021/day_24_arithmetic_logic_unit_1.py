#!/usr/bin/env python3

import sys
from typing import List


def process_program(data: List[str]):
    block = 0

    print("z0 = 0")
    print()

    for i in range(0, len(data), 18):
        print(f"block {block + 1}")

        magic_number_1 = int(data[i + 4].split()[2])
        magic_number_2 = int(data[i + 5].split()[2])
        magic_number_3 = int(data[i + 15].split()[2])

        if magic_number_2 >= 10 and magic_number_1 == 1:
            print(f"z{block + 1} = z{block} * 26 + w{block + 1} + {magic_number_3}")

        if magic_number_2 < 10:
            print(f"w{block + 1} = z{block} % 26 + {magic_number_2}")
            print(f"z{block + 1} = z{block} / {magic_number_1}")

        block += 1
        print()


def main():
    data = [x.strip('\n') for x in sys.stdin]
    process_program(data)


if __name__ == '__main__':
    main()
