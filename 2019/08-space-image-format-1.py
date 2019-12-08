#!/usr/bin/env python3

import sys
import numpy as np


def control_value(layers):
    min_cnt_0 = layers.shape[1] * layers.shape[2] + 1
    result = -1

    for ind in range(layers.shape[0]):
        layer = layers[ind]
        cnt_0 = layer[layer == 0].shape[0]

        if cnt_0 < min_cnt_0:
            min_cnt_0 = cnt_0
            result = layer[layer == 1].shape[0] * layer[layer == 2].shape[0]

    return result


def parse_input(data, width, height):
    layers_cnt = int(len(data) / width / height)
    layers = np.zeros((layers_cnt, height, width))

    ind = 0

    for layer in range(layers_cnt):
        for i in range(height):
            for j in range(width):
                layers[layer][i][j] = int(data[ind])
                ind += 1

    return layers


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    width = 25
    height = 6

    layers = parse_input(data, width, height)
    result = control_value(layers)

    print(result)
