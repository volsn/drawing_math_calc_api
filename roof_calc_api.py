#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import polygon
import side
import extras
import copy
import math
from flask_cors import CORS

import pprint
PP = pprint.PrettyPrinter(indent=2)

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


def parse_holes(shapes):

    for shape in shapes:
        if shape['isHole'] == True:
            for line in shapes['line']:

                    line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                            math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))
                    line['length_real'] = line['length_plan']

            shape[square] = polygon.calc_square(shape, angle=0)

    return shapes


def parse_min_shapes(shapes):

    for shape in shapes:
        shape['angle'] = 0
        shape['square'] = polygon.calc_square(shape, shape['angle'])

    return shapes


def parse_shapes(shapes):
    """
    Function that parses shape array fulfilling all the data about shpape where it is possible
    :param shapes: list
    :return: list
    """

    for shape in shapes:
        if polygon.is_shape_valid(shape) and shape['isHole'] != False:
            if shape['angle'] is None:
                shape['angle'] = polygon.calc_angle(shape)
            shape['square'] = polygon.calc_square(shape, shape['angle'])
    return shapes


def parse_lines(shapes):
    """
    Function that parses lines array fulfilling all the data about line where it is possible
    :param shapes: list
    :return: list
    """

    lines = list(extras.exact_lines(shapes).values()) # a dict containing information about all the lines
    lines_to_check = [] # list of lines that are about to be solved
    checked_lines = [] # list of lines that are already solved

    lines_to_check = side.check_lines(lines, checked_lines)

    while len(lines_to_check) != 0:

        print(lines_to_check)

        for id in lines_to_check:

            i = extras.find_element_by_id(id, lines)
            checked_line = side.solve_line(lines[i])
            checked_lines.append(id)
            lines[i] = checked_line

            points = extras.exact_coords(lines)

            for line in lines:
                if line['id'] not in checked_lines:
                    if checked_line['points'][0]['z'] is not None:
                        if line['points'][0]['id'] == checked_line['points'][0]['id']:
                            line['points'][0] = checked_line['points'][0]
                        if line['points'][1]['id'] == checked_line['points'][0]['id']:
                            line['points'][1] = checked_line['points'][0]
                    if checked_line['points'][1]['z'] is not None:
                        if line['points'][0]['id'] == checked_line['points'][1]['id']:
                            line['points'][0] = checked_line['points'][1]
                        if line['points'][1]['id'] == checked_line['points'][1]['id']:
                            line['points'][1] = checked_line['points'][1]

        lines_to_check = side.check_lines(lines, checked_lines)

    # Set values of lines to shapes
    for shape in shapes:
        answer = []
        for line in shape['lines']:
            answer.append(lines[
                extras.find_element_by_id(line['id'], lines)
            ])

        shape['lines'] = answer

    return shapes


def parse_points(shapes):

    lines = list(extras.exact_lines(shapes).values())
    cornice_points = []

    cornice_height = 0

    # Setting cornice height
    for line in lines:
        if line['type'] == 'cornice':
            for point in line['points']:
                cornice_points.append(point['id'])
                if point['z'] is not None:
                    cornice_height = point['z']

    for line in lines:
        for point in line['points']:
            if point['id'] in cornice_points:
                point['z'] = cornice_height

    for shape in shapes:
        answer = []
        for line in shape['lines']:
            answer.append(lines[
                extras.find_element_by_id(line['id'], lines)
            ])

        shape['lines'] = answer

    for shape in shapes:
        if shape['angle'] is not None:

            not_vertical_line = None
            vertical_line = None

            for line in shape['lines']:
                if line['type'] != 'cornice' and line['type'] != 'gable':
                    not_vertical_line = line
            for line in shape['lines']:
                if line['type'] == 'cornice' or line['type'] == 'gable':
                    vertical_line = line

            x1 = vertical_line['points'][0]['x']
            y1 = vertical_line['points'][0]['y']
            x2 = vertical_line['points'][1]['x']
            y2 = vertical_line['points'][1]['y']

            if not_vertical_line['points'][0]['z'] is None:
                x3 = not_vertical_line['points'][0]['x']
                y3 = not_vertical_line['points'][0]['y']
            else:
                x3 = not_vertical_line['points'][1]['x']
                y3 = not_vertical_line['points'][1]['y']

            px = x2 - x1
            py = y2 - y1
            dab = px * px + py * py

            u = ((x3 - x1) * px + (y3-y1) * py) / dab
            x = x1 + u * px
            y = y1 + u * py

            length_plan = math.sqrt((x3 - x) * (x3 - x) + (y3 - y) * (y3 - y))

            if not_vertical_line['points'][0]['z'] is None:
                not_vertical_line['points'][0]['z'] = length_plan * math.tan(math.radians(shape['angle'])) + \
                                                      not_vertical_line['points'][1]['z']
            else:
                not_vertical_line['points'][1]['z'] = length_plan * math.tan(math.radians(shape['angle'])) + \
                                                      not_vertical_line['points'][0]['z']

            for line in lines:
                if line['id'] == not_vertical_line['id']:
                    lines[
                        extras.find_element_by_id(line['id'], lines)
                    ] = not_vertical_line

    return shapes


def calc_real_length(shapes_orig, shapes_solved):

    lines_orig = list(extras.exact_lines(shapes_orig).values())
    lines_solved = list(extras.exact_lines(shapes_solved).values())

    koefficient = 1
    for line in lines_orig:
        if line['length_real'] is not None:
            id = line['id']
            line_num = extras.find_element_by_id(id, lines_solved)
            koefficient = line['length_real'] / lines_solved[line_num]['length_real']
        elif line['length_plan'] is not None:
            id = line['id']
            line_num = extras.find_element_by_id(id, lines_solved)
            koefficient = line['length_plan'] / lines_solved[line_num]['length_plan']

    if koefficient == 1:
        for shape in shapes_orig:
            if shape['square'] is not None:
                id = shape['id']
                shape_num = extras.find_element_by_id(id, shapes_solved)
                koefficient = math.sqrt(shape['square'] / shapes_solved[shape_num]['square'])
                break

    for line in lines_solved:
        line['length_real'] *= koefficient
        line['length_plan'] *= koefficient


    # Set koefficient to calculate real shapes lengths
    koefficient = koefficient * koefficient

    for shape in shapes_solved:
        answer = []
        for line in shape['lines']:
            answer.append(lines_solved[
                extras.find_element_by_id(line['id'], lines_solved)
            ])

        shape['lines'] = answer

        if shape['square'] is not None:
            shape['square'] *= koefficient

    return shapes_solved


def _is_shapes_valid(shapes):

    for shape in shapes:
        if shape['angle'] is not None:
            return True

    return False


class Index(Resource):
    def post(self):
        json = request.json
        original = copy.deepcopy(json['shapes'])
        json['shapes'] = parse_points(json['shapes'])
        json['shapes'] = parse_lines(json['shapes'])
        json['shapes'] = parse_holes(json['shapes'])

        if _is_shapes_valid(json['shapes']):
            json['shapes'] = parse_shapes(json['shapes'])
        else:
            json['shapes'] = parse_min_shapes(json['shapes'])

        json['shapes'] = calc_real_length(original, json['shapes'])
        return jsonify(json)

    def get(self):
        return jsonify({'message': 'Hello, world!'})


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
