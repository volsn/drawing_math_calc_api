from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import polygon
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


class Roof(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument(PARAMETER_NAME, required=True, location='json')
        args = parser.parse_args()
        data = json.loads(args[PARAMETER_NAME])
