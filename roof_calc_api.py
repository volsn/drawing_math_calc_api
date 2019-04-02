from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import polygon
import side
import extras

import pprint
PP = pprint.PrettyPrinter(indent=2)

app = Flask(__name__)
api = Api(app)


def parse_shapes(shapes):
    """
    Function that parses shape array fulfilling all the data about shpape where it is possible
    :param shapes: list
    :return: list
    """

    for shape in shapes:
        if polygon.is_shape_valid(shape):
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

    has_cornice_z = False
    for id in lines_to_check:
        i = extras.find_element_by_id(id, lines)
        if lines[i]['type'] == 'cornice':
            has_cornice_z = True

    if not has_cornice_z:
        for line in lines:
            if line['type'] == 'cornice':
                for point in line['points']:
                    point['z'] = 0
        lines_to_check = side.check_lines(lines, checked_lines)


    while len(lines_to_check) != 0:

        lines_to_check_ = []
        for id in lines_to_check:
            i = extras.find_element_by_id(id, lines)
            if lines[i]['type'] == 'cornice':
                lines_to_check_.insert(0, lines[i]['id'])
        for id in lines_to_check:
            i = extras.find_element_by_id(id, lines)
            if lines[i]['type'] != 'cornice':
                lines_to_check_.append(lines[i]['id'])
        lines_to_check = lines_to_check_


        for id in lines_to_check:
            i = extras.find_element_by_id(id, lines)
            checked_line = side.solve_line(lines[i])
            checked_lines.append(id)

            lines[i] = checked_line

            # Set values of points of checked lines to lines that cross with it
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


def calc_real_length(shapes_orig, shapes_solved):

    print(shapes_orig)

    lines_orig = list(extras.exact_lines(shapes_orig).values())
    lines_solved = list(extras.exact_lines_from_single_shape(shapes_solved).values())

    koefficient = 1
    for line in lines_orig:
        if line['length_real'] is not None:
            id = line['id']
            line_num = extras.find_element_by_id(id, lines_solved)
            koefficient = line['length_real'] / lines_solved[line_num]['length_real']
        elif line['length_plan'] is not None:
            id = line['id']
            line_num = extras.find_element_by_id(id, lines_solved)
            koefficient = line['length_real'] / lines_solved[line_num]['length_real']


    for line in lines_solved:
        line['length_real'] *= koefficient
        line['length_plan'] *= koefficient


    for shape in shapes_solved:
        answer = []
        for line in shape['lines']:
            answer.append(lines_solved[
                extras.find_element_by_id(line['id'], lines_solved)
            ])

        shape['lines'] = answer

    return shapes_solved


class Index(Resource):
    def post(self):
        json = request.json
        original = json
        json['shapes'] = parse_lines(json['shapes'])
        json['shapes'] = parse_shapes(json['shapes'])
        return jsonify(json)

    def get(self):
        return jsonify({'message': 'Hello, world!'})


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
