import math
import extras
import line


def calc_shapes(shapes):

    warning_shapes = []

    for i, shape in enumerate(shapes):
        if shape['angle'] is not None:

            square = calc_square(shape, angle)
            shapes[i]['square'] = square

        else:

            if is_valid(shape):

                angle = calc_angle(shape)

                #print(angle)

                if angle is False:
                    warning_shapes.append(shape['id'])
                else:

                    shapes[i]['angle'] = angle
                    square = calc_square(shape, angle)
                    shapes[i]['square'] = square

            else:
                warning_shapes.append(shape['id'])

    return shapes, warning_shapes


def is_valid(shape):

    points = 0
    for point in shape['vertices']:
        if point['z'] is not None:
            points += 1

    if points >= 3:
        return True
    else:
        return False


def calc_angle(shape):

    # Extracting three points A, B and C from a plane
    # in order to build the plane`s formula

    points = {}

    for point in shape['vertices']:
        if point['z'] not in points.keys() and point['z'] is not None:
            points[str(point['z'])] = point['id']

    if len(points) == 2:
        for point in shape['vertices']:
            if point['id'] not in points.values() and point['z'] is not None:
                points['-100500'] = point['id']

    print(points)

    lines = list(extras.exact_lines_from_single_shape(shape.copy()).values())
    all_points = list(extras.exact_coords(lines).values())

    plane_coords = []
    for i, point in enumerate(points.values()):
        for point_ in all_points:
            if point_['id'] == point:

                if point_['z'] is not None:
                    plane_coords.append(point_)
                else:
                    for point_vert in shape['vertices']:
                        if point_vert['id'] == point_['id']:
                            point_['z'] = point_vert['z']
                            plane_coords.append(point_)
                            continue

                    return False


    if len(plane_coords) < 3:
        return False

    print(plane_coords)

    plane_coords = plane_coords[:3]
    plane_equation = _build_plane_equation(plane_coords)

    vertical_plane_equation = [0,0,1,0]

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

    x = []
    y = []
    for point in points:
        x.append(point['x'])
        y.append(point['y'])

    plan_square = abs(sum(x[i] * (y[i + 1] - y[i - 1]) for i in range(-1, len(x) - 1))) / 2.0
    real_square = plan_square / math.cos(math.radians(angle))

    return real_square


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
