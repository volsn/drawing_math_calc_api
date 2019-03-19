from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import polygon
import side
import extras

PORT = 5002
PARAMETER_NAME = 'test_api'


app = Flask(__name__)
api = Api(app)


def parse_shapes(shapes):
    for shape in shapes:
        coords = extras.exact_coords(shape['lines'])
        shape['square'] = polygon.polygon_square(coords)
    return shapes


def parse_lines(shapes):

    lines = extras.exact_lines(shapes) # a dict containing information about all the lines
    lines_to_check = [] # list of lines that are about to be solved
    checked_lines = [] # list of lines that are already solved

    lines_to_check = side.check_lines(lines, checked_lines)

    while lines_to_check is not []:

        for id in lines_to_check:
            i = extras.find_element_by_id(lines, id)
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


class Roof(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument(PARAMETER_NAME, required=True, location='json')
        args = parser.parse_args()
        data = json.loads(args[PARAMETER_NAME])
