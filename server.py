#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import copy
import math
from flask_cors import CORS
import line
import shape
import extras


app = Flask(__name__)
cors = CORS(app)
api = Api(app)


class Index(Resource):
    def post(self):
        json = request.json
        shapes = json['shapes']
        original = copy.deepcopy(shapes)
        shapes, warnings_lines = line.calc_lines(shapes)
        shapes, warning_shapes = shape.calc_shapes(shapes)
        shapes, koefficient = extras.calc_real_length(original, shapes)

        warnings = {'lines': warnings_lines, 'shapes': warning_shapes}

        if koefficient == 1:
            warnings['no_koefficient'] = True


        result = {}
        result['shapes'] = shapes
        result['warning'] = warnings

        return result


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
