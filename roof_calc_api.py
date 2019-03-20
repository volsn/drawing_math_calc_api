from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import polygon
import side
import extras


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

    while len(lines_to_check) != 0:

        for id in lines_to_check:
            i = extras.find_element_by_id(id, lines)
            checked_line = side.solve_line(lines[i])
            checked_lines.append(id)

            lines[i] = checked_line

            # Set values of points of the checked lines to lines that cross with it
            for point in checked_line['points']:
                for line_ in lines:
                    for point_ in line_['points']:
                        if point_['id'] == point['id']:
                            point_ = point

            del(id)

        lines_to_check = side.check_lines(lines, checked_lines)

    # Set values of lines to shapes
    for shape in shapes:
        for line in shape['lines']:
            line = lines[
                extras.find_element_by_id(line['id'], lines)
            ]

    return shapes


class Index(Resource):
    def post(self):

        json = request.get_json()
        json['lines'] = parse_lines(json['shapes'])
        json['shapes'] = parse_shapes(json['shapes'])
        return jsonify(json)

    def get(self):
        return jsonify({'message': 'Hello, world!'})


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
