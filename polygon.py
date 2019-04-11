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

    lines_types = {}

    for line in shape['lines']:
        if not side._check_line(line):
            return False
        return True


def _build_plane_equation(points):

    points_ = []
    i = 0
    for point in points:
        points_.append([])
        points_[i].append(point['x'])
        points_[i].append(point['y'])
        points_[i].append(point['z'])
        i += 1
    points = points_

    C = [None] * 3

    # Finding coords of two vectors on the plane
    vectorAB = [None] * 3
    vectorAC = [None] * 3

    for coord in range(3):
        vectorAB[coord] = points[1][coord] - points[0][coord]
        vectorAC[coord] = points[2][coord] - points[0][coord]
        C[coord] = points[2][coord]


    # Looking for the normal
    normal = [None] * 3
    normal[0] = vectorAB[1] * vectorAC[2] - vectorAB[2] * vectorAC[1]
    normal[1] = vectorAB[2] * vectorAC[0] - vectorAB[0] * vectorAC[2]
    normal[2] = vectorAB[0] * vectorAC[1] - vectorAB[1] * vectorAC[0]


    # Building the final plane equation
    equation = [None] * 4
    equation[0] = normal[0]
    equation[1] = normal[1]
    equation[2] = normal[2]
    equation[3] = -1 * normal[0] * C[0] + -1 * normal[1] * C[1] + \
                  -1 * normal[2] * C[2]

    return equation



def calc_angle(shape):

    # Extracting three points A, B and C from a plane
    # in order to build the plane`s formula
    lines = list(extras.exact_lines_from_single_shape(shape.copy()).values())

    plane_coords = []

    for line in lines:
        if line['type'] == 'cornice':
            plane_coords.append(line['points'][0].copy())
            plane_coords.append(line['points'][1].copy())
            break

    for line in lines:
        if line['type'] == 'skate':
            if line['points'][0]['z'] > line['points'][1]['z']:
                print('bar')
                plane_coords.append(line['points'][0].copy())
            else:
                plane_coords.append(line['points'][1].copy())
            break

    plane_equation = _build_plane_equation(plane_coords)

    plane_coords[2]['z'] = 0
    vertical_plane_equation = _build_plane_equation(plane_coords)
    print(plane_coords)

    angle = math.degrees(math.acos(
            abs(plane_equation[0] * vertical_plane_equation[0] + \
                 plane_equation[1] * vertical_plane_equation[1] + \
                 plane_equation[2] * vertical_plane_equation[2]) / \
            math.sqrt(
                (math.pow(plane_equation[0], 2) + \
                    math.pow(plane_equation[1], 2) + \
                    math.pow(plane_equation[2], 2)) * \
                (math.pow(vertical_plane_equation[0], 2) + \
                    math.pow(vertical_plane_equation[1], 2) + \
                    math.pow(vertical_plane_equation[2], 2))
        )))

    return angle


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

    nbCoordinates = len(coords)
    nbSegment = nbCoordinates - 1

    plan_square = [(coords[i + 1][0] - coords[i][0]) * (coords[i + 1][1] + coords[i][1]) for i
         in range(nbSegment)]

    plan_square = abs(sum(plan_square) / 2.)

    if angle == 0:
        return plan_square
    else:
        real_square = plan_square * math.cos(math.radians(angle))
        return real_square


if __name__ == '__main__':

    plane1 = [-400, -64200, -37105, 22533600]
    plane2 = [0, 0, -37105, 0]

    plane = _build_plane_equation(points)
