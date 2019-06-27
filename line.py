import math
import extras

def calc_lines(shapes):

    vertices_points = extras.extract_vertices(shapes)
    lines = extras.extract_lines(shapes)

    warnings_lines = {}

    """for id, line in lines.items():
        for i, point in enumerate(line['points']):
            if point['id'] in vertices_points.keys():
                lines[id]['points'][i]['z'] = vertices_points[point['id']]"""

    for i, shape in enumerate(shapes):
        for j, line in enumerate(shape['lines']):
            for k, point in enumerate(line['points']):
                if point['id'] in vertices_points.keys():
                    shapes[i]['lines'][j]['points'][k]['z'] = vertices_points[point['id']]

    for i, shape in enumerate(shapes):
        for j, line in enumerate(shape['lines']):
            if is_valid(line):
                shapes[i]['lines'][j] = calc_line(line)
            else:
                if shape['id'] in warnings_lines.keys():
                    warnings_lines[shape['id']].append(line['id'])
                else:
                    warnings_lines[shape['id']] = [line['id']]

    return shapes, warnings_lines


def is_valid(line):
    """
    Checks whether the given line can be solved
    :param line: dict
    :return: bool
    """

    if line['type'] == 'edge' or line['type'] == 'endova':

        # Line has an angle
        if line['angle'] is not None:
            return True
        # Line has all the coordinates
        if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:
            return True

        if line['length_real'] is not None and line['length_plan'] is not None:
            return True


    elif line['type'] == 'gable' or line['type'] == 'roof_fracture':

        # Line has all the coordinates
        if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:
            return True


    elif line['type'] == 'skate':

        # Line has all the coordinates
        for point in line['points']:
            if point['z'] is not None:
                return True

    elif line['type'] == 'cornice':

        return True


    return False


def calc_line(line):
    """
    Solves the given line(finds real and plan length, angle and coords of top)
    :param line: dict
    :return: dict
    """

    if line['type'] == 'edge' or line['type'] == 'endova':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        if line['angle'] is not None:
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            if line['points'][0]['z'] is None:
                line['points'][0]['z'] = line['length_plan'] * math.tan(math.radians(line['angle'])) + line['points'][1]['z']
            elif line['points'][1]['z'] is None:
                line['points'][1]['z'] = line['length_plan'] * math.tan(math.radians(line['angle'])) + line['points'][0]['z']

        elif line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:

            if line['points'][0]['z'] > line['points'][1]['z']:
                line['angle'] = abs(math.degrees(math.atan((line['points'][0]['z'] - line['points'][1]['z']) \
                        / line['length_plan'])))
                line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            else:

                line['angle'] = abs(math.degrees(math.atan((line['points'][1]['z'] - line['points'][0]['z']) / line['length_plan'])))
                line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

    elif line['type'] == 'cornice':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))


        line['length_real'] = line['length_plan']

    elif line['type'] == 'skate':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        line['length_real'] = line['length_plan']

        for point in line['points']:
            if point['z'] is not None:
                z = point['z']
        line['points'][0]['z'] = z
        line['points'][1]['z'] = z


    elif line['type'] == 'gable' or line['type'] == 'roof_fracture':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        if line['angle'] is not None:
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            if line['points'][0]['z'] is None:
                line['points'][0]['z'] = line['length_plan'] * math.tan(math.radians(line['angle'])) + \
                                         line['points'][1]['z']
            elif line['points'][1]['z'] is None:
                line['points'][1]['z'] = line['length_plan'] * math.tan(math.radians(line['angle'])) + \
                                         line['points'][0]['z']

        elif line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:

            if line['points'][0]['z'] > line['points'][1]['z']:
                line['angle'] = abs(math.degrees(math.atan((line['points'][0]['z'] - line['points'][1]['z']) \
                                                           / line['length_plan'])))
                line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            else:

                line['angle'] = abs(
                    math.degrees(math.atan((line['points'][1]['z'] - line['points'][0]['z']) / line['length_plan'])))
                line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))


    return line
