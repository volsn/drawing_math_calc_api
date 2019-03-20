import sys
import side
import extras
import math


def is_shape_valid(shape):

    for line in shape['lines']:
        if line['type'] == 'ridge' or line['type'] == 'ending':
            if not side._check_line(line):
                return False
    return True


def calc_angle(shape):

    lines = list(extras.exact_lines_from_single_shape(shape).values())

    for line in lines:
        if line['type'] == 'ridge' or line['type'] == 'ending':
            for point in line['points']:
                if point['z'] != 'null':
                    roof_line_coords = point
                else:
                    base_line_coords = point

    height_coords = {
        'x': base_line_coords['x'],
        'y': roof_line_coords['y'],
        'z': 0,
    }

    deltaY = roof_line_coords['y'] - height_coords['y']
    deltaX = roof_line_coords['x'] - height_coords['x']
    angle_to_x_axis = math.atan2(deltaY, deltaX) * 180 / math.pi

    height_coords['x'] = height_coords['x'] * math.cos(angle_to_x_axis) - \
                    height_coords['y'] * math.sin(angle_to_x_axis)
    height_coords['y'] = height_coords['x'] * math.sin(angle_to_x_axis) + \
                    height_coords['y'] * math.cos(angle_to_x_axis)


    line = {
        'angle': 'null',
        'points':[
            roof_line_coords,
            height_coords,
        ],
        'type': 'technical_line',
        'length_plan': 'null',
        'length_real': 'null',
    }
    line = side.solve_line(line)

    return line['angle']


def _polygon_plan_square(coords):
    pass


def calc_square(shape, angle):

    lines = list(extras.exact_lines_from_single_shape(shape).values())
    points = list(extras.exact_coords(lines).values())

    coords = []
    for point in points:
        x = point['x']
        y = point['y']
        coords.append(tuple([x, y]))

    n = len(coords)
    plan_square = 0.0

    for i in range(n):

        j = (i + 1) % n
        plan_square += coords[i][0] * coords[j][1]
        plan_square -= coords[j][0] * coords[i][1]

    plan_square = abs(plan_square) / 2.0
    real_square = plan_square * math.cos(math.radians(angle))

    return real_square


"""
For test purpose
"""

if __name__ == '__main__':

    line1 = {
        'id': 1,
        'angle': 'null',
        'points': [
            {
                'id': 1,
                'x': 1,
                'y': 5,
                'z': 'null',
            },
            {
                'id': 2,
                'x': 1,
                'y': 3,
                'z': 'null',
            },
        ],
        'type': 'base',
        'length_plan': 'null',
        'length_real': 'null',
    }
    line2 = {
        'id': 2,
        'angle': 'null',
        'points': [
            {
                'id': 1,
                'x': 1,
                'y': 5,
                'z': 'null',
            },
            {
                'id': 3,
                'x': 3,
                'y': 7,
                'z': 4,
            },
        ],
        'type': 'ridge',
        'length_plan': 'null',
        'length_real': 'null',
    }
    line3 = {
        'id': 3,
        'angle': 'null',
        'points': [
            {
                'id': 2,
                'x': 1,
                'y': 3,
                'z': 'null',
            },
            {
                'id': 3,
                'x': 3,
                'y': 7,
                'z': 4,
            },
        ],
        'type': 'ridge',
        'length_plan': 'null',
        'length_real': 'null',
    }

    shape = {
        'lines': [
            line1,
            line2,
            line3,
        ],
    }