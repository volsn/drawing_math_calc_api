import math
import sys


def _check_line(line):
    """
    Checks whether the given line can be solved
    :param line: dict
    :return: bool
    """

    if line['type'] == 'skate' or line['type'] == 'endova':

        if line['length_real'] is not None:
            return True
        if line['angle'] is not None:
            if line['points'][0]['z'] is not None or line['points'][1]['z'] is not None:
                return True
        if line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:
            return True

        return False

    elif line['type'] == 'cornice':
        for point in line['points']:
            if point['z'] is not None and point['z'] != 0:
                return True

    elif line['type'] == 'edge':
        for point in line['points']:
            if point['z'] is not None:
                return True

    elif line['type'] == 'glabe' or line['type'] == 'roof_fracture':
        if line['angle'] is not None:
            for point in line['points']:
                if point['z'] is not None:
                    return True
        elif line['points'][0]['z'] is not None and line['points'][1]['z'] is not None:
            return True


    return False


def check_lines(lines, checked_lines):
    """
    Returns a list of ids of lines that can be solved
    :param lines: list
    :return: list
    """

    valide_lines = []

    for line in lines:
        if line['id'] not in checked_lines and _check_line(line):
            valide_lines.append(line['id'])
    return valide_lines


def solve_line(line):
    """
    Solves the given line(finds real and plan length, angle and coords of top)
    :param line: dict
    :return: dict
    """

    if line['type'] == 'skate' or line['type'] == 'endova':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        if line['angle'] is not None:
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            height = 0
            for point in line['points']:
                if point['z'] is None:
                    height = line['length_plan']  * math.tan(math.radians(line['angle']))

            if line['points'][0]['z'] is None:
                line['points'][0]['z'] = height + line['points'][1]['z']
            elif line['points'][1]['z'] is None:
                line['points'][1]['z'] = height + line['points'][0]['z']


        elif line['length_real'] is not None:
            line['angle'] = math.degrees(math.acos(line['length_plan'] / line['length_real']))

            for point in line['points']:
                if point['z'] is not None:
                    point['z'] = line['length_plan']  * math.tan(math.radians(line['angle']))
                else:
                    point['z'] = 0
        elif line['points'][0]['z'] is not None:

            line['angle'] = math.degrees(math.atan((line['points'][0]['z'] - line['points'][1]['z']) / line['length_plan']))
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][0]['z'] is None:
            line['points'][0]['z'] = 0
        elif line['points'][1]['z'] is not None:

            line['angle'] = math.degrees(math.atan((line['points'][1]['z'] - line['points'][0]['z']) / line['length_plan']))
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][1]['z'] is None:
            line['points'][1]['z'] = 0
    elif line['type'] == 'cornice':

        if line['points'][0]['z'] is None:
            line['points'][0]['z'] = 0
        if line['points'][1]['z'] is None:
            line['points'][1]['z'] = 0

        if line['points'][0]['z'] != line['points'][1]['z']:
            if line['points'][0]['z'] == 0:
                line['points'][0]['z'] = line['points'][1]['z']
            else:
                line['points'][1]['z'] = line['points'][0]['z']


        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        line['length_real'] = line['length_plan']

    elif line['type'] == 'edge':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        line['length_real'] = line['length_plan']

        for point in line['points']:
            if point['z'] is not None:
                z = point['z']
        line['points'][0]['z'] = z
        line['points'][1]['z'] = z

    elif line['type'] == 'glabe' or line['type'] == 'roof_fracture':

        if line['angle'] is not None:
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))

            height = 0
            for point in line['points']:
                if point['z'] is None:
                    height = line['length_plan'] * math.tan(math.radians(line['angle']))

            if line['points'][0]['z'] is None:
                line['points'][0]['z'] = height + line['points'][1]['z']
            elif line['points'][1]['z'] is None:
                line['points'][1]['z'] = height + line['points'][0]['z']

        elif line['points'][0]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][0]['z'] / line['length_plan']))
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][0]['z'] is None:
            line['points'][0]['z'] = 0
        elif line['points'][1]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][1]['z'] / line['length_plan']))
            line['length_real'] = line['length_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][1]['z'] is None:
            line['points'][1]['z'] = 0

    return line
