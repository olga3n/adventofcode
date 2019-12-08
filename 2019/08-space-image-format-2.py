#!/usr/bin/env python3

import sys
import numpy as np


def stack_layers(layers):
    min_cnt_0 = layers.shape[1] * layers.shape[2] + 1
    result = np.full((layers.shape[1], layers.shape[2]), 2)

    for ind in range(layers.shape[0]):
        for i in range(layers[ind].shape[0]):
            for j in range(layers[ind].shape[1]):
                if result[i][j] == 2:
                    result[i][j] = layers[ind][i][j]

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


class TestClass:
    def test_stack_layers_1(self):
        layers = parse_input('0222112222120000', 2, 2)
        result = stack_layers(layers)

        assert np.array_equal(result, np.array([[0, 1], [1, 0]]))


if __name__ == '__main__':
    data = sys.stdin.readline().strip()

    width = 25
    height = 6

    layers = parse_input(data, width, height)
    result = stack_layers(layers)

    for i in range(result.shape[0]):
        line = ''
        for j in range(result.shape[1]):
            if result[i][j] == 1:
                line += '■'
            else:
                line += ' '
        print(line)
