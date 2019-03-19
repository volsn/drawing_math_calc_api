import math
import sys


def _check_line(line):
    """
    Checks whether the given line can be solved
    :param line: dict
    :return: bool
    """

    if line['type'] == 'ridge' or line['type'] == 'ending':

        if line['length_real'] != 'null' and line['length_plan'] != 'null':
            return True
        if line['angle'] != 'null':
            return True
        for point in line['points']:
            if point['z'] != 'null':
                return True
        return False


def check_lines(lines, checked_lines):
    """
    Returns a list of ids of lines that can be solved
    :param lines: list
    :return: list
    """

    lines_to_be_checked = []
    for line in lines:
        if _check_line(line) and line['id'] not in checked_lines:
            lines_to_be_checked.append(line['id'])


def solve_line(line):
    """
    Solves the given line(finds real and plan length, angle and coords of top)
    :param line: dict
    :return: dict
    """


    if line['type'] == 'ridge':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x']) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y']))

        if line['angle'] != 'null':
            line['length_real'] = line['length_plan'] * math.cos(line['angle'])

            for point in line['points']:
                if point['z'] == 'null':
                    point['z'] = line['length_plan']  * math.tan(line['angle'])

        elif line['length_plan'] != 'null' and line['length_real'] != 'null':
            line['angle'] = math.acos(line['length_real'] / line['length_plan'])

            for point in line['points']:
                if point['z'] == 'null':
                    point['z'] = line['length_plan']  * math.tan(line['angle'])
        elif line['points'][0]['z'] == 'null':

            line['angle'] = math.atan(line['points'][0]['z'] / line['length_plan'])
            line['length_real'] = line['length_plan'] * math.cos(line['angle'])
        elif line['points'][1]['z'] == 'null':

            line['angle'] = math.atan(line['points'][1]['z'] / line['length_plan'])
            line['length_real'] = line['length_plan'] * math.cos(line['angle'])

    elif line['type'] == 'cornice':

        line['length_plan'] = math.sqrt(math.pow(line['points'][0]['x'] - line['points'][1]['x']) + \
                                        math.pow(line['points'][0]['y'] - line['points'][1]['y']))

    return line


def find_line_crossing(line, lines):
    """
    Returns list of lines` ids that cross with the given one
    :param line: dict
    :param lines: list
    :return: list
    """

    pass
