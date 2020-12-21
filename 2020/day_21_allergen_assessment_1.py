#!/usr/bin/env python3

import sys


def parse_records(data):
    records = []

    for line in data:
        first, second = line.split(' (contains ')

        ingredients = first.split(' ')
        allergens = second[:-1].split(', ')

        records.append((set(ingredients), set(allergens)))

    return records


def ingredients_without_allergens(data):
    start_records = parse_records(data)
    records = start_records.copy()

    ingredients_dict = {}
    allergens_dict = {}

    allergens_count = len({y for x in records for y in x[1]})

    while len(allergens_dict) < allergens_count:

        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                ingredients = records[i][0].intersection(records[j][0])
                allergens = records[i][1].intersection(records[j][1])

                ingredients = {
                    x for x in ingredients if x not in ingredients_dict
                }

                allergens = {
                    x for x in allergens if x not in allergens_dict
                }

                if len(ingredients) == 1 and len(allergens) == 1:
                    ingredient = ingredients.pop()
                    allergen = allergens.pop()

                    ingredients_dict[ingredient] = allergen
                    allergens_dict[allergen] = ingredient

                elif len(ingredients) and len(allergens):
                    records.append((ingredients, allergens))

        new_records = []

        for record in records:
            ingredients = {x for x in record[0] if x not in ingredients_dict}
            allergens = {x for x in record[1] if x not in allergens_dict}

            if len(ingredients) == 1 and len(allergens) == 1:
                ingredient = ingredients.pop()
                allergen = allergens.pop()

                ingredients_dict[ingredient] = allergen
                allergens_dict[allergen] = ingredient

            if len(allergens):
                new_records.append(record)

        records = new_records

    result = 0

    for record in start_records:
        result += len({x for x in record[0] if x not in ingredients_dict})

    return result


class TestClass():

    def test_ingredients_without_allergens(self):

        data = [
            'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
            'trh fvjkl sbzzf mxmxvkd (contains dairy)',
            'sqjhc fvjkl (contains soy)',
            'sqjhc mxmxvkd sbzzf (contains fish)'
        ]

        assert ingredients_without_allergens(data) == 5


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = ingredients_without_allergens(data)
    print(result)


if __name__ == '__main__':
    main()
