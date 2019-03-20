import sys
import side
import extras
import math


def is_shape_valid(shape):
    """
    Checks whether the given shape can be solved
    :param shape: dict
    :return: bool
    """

    for line in shape['lines']:
        if line['type'] == 'ridge' or line['type'] == 'ending':
            if not side._check_line(line):
                return False
    return True


def calc_angle(shape):
    """
    Calculates angle between the given shape and horizontal plane
    :param shape: dict
    :return: int
    """

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


def calc_square(shape, angle):
    """
    Calculates square of the given shape
    :param shape: dict
    :param angle: int
    :return: int
    """

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
