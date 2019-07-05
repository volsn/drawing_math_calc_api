import math
import extras

def calc_points(shapes):

    warning_points = {}

    for shape in shapes:
        if shape['angle'] is not None:

            points = shape['vertices']

            cornice_points = []
            valid_cornise = False
            cornice_points = []

            for line in shape['lines']:
                if line['type'] == 'cornice':
                    if line['points'][0]['z'] is not None and \
                                line['points'][1]['z'] is not None:
                        valid_cornise = line

                    for point in line['points']:
                        cornice_points.append(point['id'])

                if line['type'] == 'gable':
                    valid_cornise = None

            if valid_cornise is None or not valid_cornise:
                continue


            x1 = valid_cornise['points'][0]['x']
            y1 = valid_cornise['points'][0]['y']
            x2 = valid_cornise['points'][1]['x']
            y2 = valid_cornise['points'][1]['y']

            if x2 - x1 == 0:
                m = 0
            else:
                m = (y2 - y1) / (x2 - x1)

            b = y1 - m * x1

            for line in shape['lines']:
                for point in line['points']:
                    if point['id'] not in cornice_points:

                        x3 = point['x']
                        y3 = point['y']

                        length_plan = abs(y3 + x3 * m + b) / math.sqrt(m * m + 1)

                        if line['points'][0]['z'] is None:
                            line['points'][0]['z'] = length_plan * math.tan(math.radians(shape['angle'])) + \
                                                                  valid_cornise['points'][0]['z']
                        else:
                            line['points'][1]['z'] = length_plan * math.tan(math.radians(shape['angle'])) + \
                                                                  valid_cornise['points'][0]['z']

    return shapes


def set_vertices(shapes):

    vertices_points = extras.extract_vertices(shapes)

    for i, shape in enumerate(shapes):
        for j, line in enumerate(shape['lines']):
            for k, point in enumerate(line['points']):
                if point['id'] in vertices_points.keys() and point['z'] is None:
                    shapes[i]['lines'][j]['points'][k]['z'] = vertices_points[point['id']]

    return shapes


def set_cornice(shapes):

    for i, shape in enumerate(shapes):

        valid_cornise = True
        for line in shape['lines']:
            if line['type'] == 'gable' or line['type'] == 'roof_fracture':
                valid_cornise = False

        if valid_cornise:

            cornice_points = []
            for line in shape['lines']:
                if line['type'] == 'cornice':
                    for point in line['points']:
                        cornice_points.append(point['id'])

            cornice_height = 0
            for point in shape['vertices']:
                if point['id'] in cornice_points:
                    if point['z'] is not None:
                        cornice_height = point['z']
                        break

            for j, point in enumerate(shape['vertices']):
                if point['id'] in cornice_points:
                    shapes[i]['vertices'][j]['z'] = cornice_height

    return shapes


def calc_lines(shapes):

    lines = extras.extract_lines(shapes)

    warnings_lines = {}

    """for id, line in lines.items():
        for i, point in enumerate(line['points']):
            if point['id'] in vertices_points.keys():
                lines[id]['points'][i]['z'] = vertices_points[point['id']]"""


    for i, shape in enumerate(shapes):
        for j, line in enumerate(shape['lines']):
            if is_valid(line):
                shapes[i]['lines'][j] = calc_line(line)
            else:
                if shape['id'] in warnings_lines.keys():
                    warnings_lines[shape['id']].append(line['id'])
                else:
                    warnings_lines[shape['id']] = [line['id']]

    lines = list(extras.extract_lines(shapes).values())
    points = list(extras.exact_coords(lines).values())

    for i, shape in enumerate(shapes):
        for j, point in enumerate(shape['vertices']):
            for solved_point in points:
                if point['id'] == solved_point['id']:
                    shapes[i]['vertices'][j]['z'] = solved_point['z']

    return shapes, warnings_lines


def is_valid(line):
    """
    Checks whether the given line can be solved
    :param line: dict
    :return: bool
    """

    if line['length_real'] is not None or line['length_plan'] is not None:

        if line['type'] == 'edge' or line['type'] == 'endova' or \
                    line['type'] == 'gable' or line['type'] == 'roof_fracture':

            if line['points'][0]['z'] is not None or line['points'][1]['z'] is not None:

                # Line has all the coordinates
                if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:
                    return True

                # Line has both lengths
                if line['length_real'] is not None and line['length_plan'] is not None:
                    return True

                # Line has an angle and at least one height
                if line['angle']:
                    return True

    elif line['type'] == 'skate' or line['type'] == 'cornice':

        if line['length_plan'] is not None or line['length_real'] is not None:

            if line['points'][0]['z'] is not None or line['points'][1]['z'] is not None:
                return None



    return False


def calc_line(line):
    """
    Solves the given line(finds real and plan length, angle and coords of top)
    :param line: dict
    :return: dict
    """

    if line['type'] == 'edge' or line['type'] == 'endova' or \
                line['type'] == 'gable' or line['type'] == 'roof_fracture':

        if line['angle'] is not None and (line['length_plan'] is not None \
                        or line['length_real'] is not None):

            if line['length_real'] is not None:
                line['length_plan'] = line['length_real'] * math.cos(math.radians(line['angle']))

            elif line['length_plan'] is not None:
                line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:

                height = math.abs(line['points'][0]['z'] - line['points'][1]['z'])

                if line['length_real'] is not None:

                    line['angle'] = math.degrees(math.asin(height / line['length_real']))
                    line['length_plan'] = line['length_real'] * math.cos(math.radians(line['angle']))

                elif line['length_plan'] is not None:

                    line['angle'] = math.degrees(math.acos(height / line['length_plan']))
                    line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            elif line['points'][0]['z'] is not None:
                cornice_height = line['points'][0]['z']
                line_height = line['length_plan'] * math.tan(line['angle'])
                line['points'][1]['z'] = cornice_height + line_height

            elif line['points'][1]['z'] is not None:
                cornice_height = line['points'][1]['z']
                line_height = line['length_plan'] * math.tan(line['angle'])
                line['points'][0]['z'] = cornice_height + line_height


        elif line['length_plan'] is not None and line['length_real'] is not None:

            line['angle'] = math.degrees(math.acos(line['length_plan'] / line['length_real']))

            cornice_height = 0
            if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:

                """if line['points'][0]['z'] < line['points'][1]['z']:
                    cornice_height = line['points'][0]['z']
                    line_height = line['length_plan'] * math.tan(line['angle'])
                    line['points'][1]['z'] = cornice_height + line_height
                else:
                    cornice_height = line['points'][1]['z']
                    line_height = line['length_plan'] * math.tan(line['angle'])
                    line['points'][0]['z'] = cornice_height + line_height"""

                pass

            elif line['points'][0]['z'] is not None:
                cornice_height = line['points'][0]['z']
                line_height = line['length_plan'] * math.tan(line['angle'])
                line['points'][1]['z'] = cornice_height + line_height

            elif line['points'][1]['z'] is not None:
                cornice_height = line['points'][1]['z']
                line_height = line['length_plan'] * math.tan(line['angle'])
                line['points'][0]['z'] = cornice_height + line_height


        elif line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:

            length_plan = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                            math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

            if line['points'][0]['z'] > line['points'][1]['z']:
                line['angle'] = abs(math.degrees(math.atan((line['points'][0]['z'] - line['points'][1]['z']) \
                        / length_plan)))
                length_real = length_plan / math.cos(math.radians(line['angle']))

            else:

                line['angle'] = abs(math.degrees(math.atan((line['points'][1]['z'] - line['points'][0]['z']) / line['length_plan'])))
                length_real = length_plan / math.cos(math.radians(line['angle']))


            if line['length_plan'] is not None:
                coefficient = line['length_plan'] / length_plan
                line['length_real'] = coefficient * length_real

            if line['length_real'] is not None:
                coefficient = line['length_real'] / length_real
                line['length_plan'] = coefficient * length_plan


    elif line['type'] == 'cornice' or line['type'] == 'skate':

        line['angle'] = 0

        if line['length_plan'] is not None:
            line['length_real'] = line['length_plan']
        elif line['length_real'] is not None:
            line['length_plan'] = line['length_real']

        if line['points'][0]['z'] is not None:
            line['points'][1]['z'] = line['points'][0]['z']
        elif line['points'][1]['z'] is not None:
            line['points'][0]['z'] = line['points'][1]['z']

    return line
