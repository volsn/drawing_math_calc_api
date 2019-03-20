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

    lines = extras.exact_lines(shape)

    for line in lines.values():
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

    lines = extras.exact_lines(shape)
    coords = extras.exact_coords(lines)

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

    shape = {}

    shape['lines'] = []

    for _ in range(2):
        line = {}
        for _ in range(3):
            line['x'] = float(input())
            line['y'] = float(input())
            line['z'] = float(input())



