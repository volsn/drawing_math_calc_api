import math
import sys


def _check_line(line):
    """
    Checks whether the given line can be solved
    :param line: dict
    :return: bool
    """

    if line['type'] == 'skate' or line['type'] == 'endova':

        if line['lenght_real'] is not None:
            return True
        if line['angle'] is not None:
            return True
        for point in line['points']:
            if point['z'] is not None:
                return True
        return False

    elif line['type'] == 'cornice':
        return True
    elif line['type'] == 'edge':
        for point in line['points']:
            if point['z'] is not None:
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

        line['lenght_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        if line['angle'] is not None:
            line['lenght_real'] = line['lenght_plan'] / math.cos(math.radians(line['angle']))

            for point in line['points']:
                if point['z'] == 'null':
                    point['z'] = line['length_plan']  * math.tan(math.radians(line['angle']))

        elif line['lenght_real'] is not None:
            line['angle'] = math.degrees(math.acos(line['lenght_plan'] / line['lenght_real']))

            for point in line['points']:
                if point['z'] is not None:
                    point['z'] = line['lenght_plan']  * math.tan(math.radians(line['angle']))
        elif line['points'][0]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][0]['z'] / line['lenght_plan']))
            line['lenght_real'] = line['lenght_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][1]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][1]['z'] / line['lenght_plan']))
            line['lenght_real'] = line['lenght_plan'] / math.cos(math.radians(line['angle']))

    elif line['type'] == 'cornice':

        line['lenght_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        line['lenght_real'] = line['lenght_plan']

    elif line['type'] == 'edge':

        line['lenght_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        line['lenght_real'] = line['lenght_plan']

        for point in line['points']:
            if point['z'] is not None:
                z = point['z']
        line['points'][0]['z'] = z
        line['points'][1]['z'] = z


    elif line['type'] == 'technical_line':
        line['lenght_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x'], 2) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y'], 2))

        if line['points'][0]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][0]['z'] / line['lenght_plan']))
            line['lenght_real'] = line['lenght_plan'] / math.cos(math.radians(line['angle']))
        elif line['points'][1]['z'] is not None:

            line['angle'] = math.degrees(math.atan(line['points'][1]['z'] / line['lenght_plan']))
            line['lenght_real'] = line['lenght_plan'] / math.cos(math.radians(line['angle']))

    return line
