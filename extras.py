import math
import line

def extract_vertices(shapes):

    points = {}

    for shape in shapes:
        for point in shape['vertices']:
            if point['z'] is not None:
                points[point['id']] = point['z']

    return points


def set_points(shapes):

    vertices = {}
    points = {}

    for shape in shapes:

        for point in shape['vertices']:
            vertices[point['id']] = point

        lines = list(exact_lines_from_single_shape(shape).values())

        for line_ in lines:
            for point in line_['points']:
                if point['z'] is not None:
                    points[point['id']] = point['z']

    for id, point_vertice in vertices.items():
        if point_vertice['z'] is None and point_vertice['id'] in points.keys():
            point_vertice['z'] = points[point_vertice['id']]


    for i, shape in enumerate(shapes):
        for j, point in enumerate(shape['vertices']):
            if point['id'] in vertices.keys():
                shapes[i]['vertices'][j] = vertices[point['id']]['z']

    #shapes = line.set_vertices(shapes)

    return shapes


def calc_roof_detailed(shapes):

    angles_squares = {}

    for shape in shapes:
        if shape['angle'] is not None and shape['square'] is not None:
            if shape['angle'] not in angles_squares.keys():
                angles_squares[shape['angle']] = 0
            angles_squares[shape['angle']] += shape['square']


    lens_lines = {}

    for shape in shapes:
        for line in shape['lines']:
            if line['length_real'] is not None:
                if line['type'] not in lens_lines.keys():
                    lens_lines[line['type']] = 0

                lens_lines[line['type']] += line['length_real']

    result = {'squares': angles_squares, 'lengths': lens_lines}

    return result


def extract_lines(shapes):

    extracted_lines = {}

    for shape in shapes:
        for line in shape['lines']:
            id = line['id']
            if id not in extracted_lines.keys():
                extracted_lines[id] = line
            """else:
                if extracted_lines[id]['points'][0]['z'] is None:
                    extracted_lines[id]['points'][0]['z'] = line['points'][0]['z']
                if extracted_lines[id]['points'][1]['z'] is None:
                    extracted_lines[id]['points'][1]['z'] = line['points'][1]['z']
                if extracted_lines[id]['angle'] is None:
                    extracted_lines[id]['angle'] = line['angle']
                    """
    return extracted_lines

def find_koefficient(lines_orig, lines_solved):

    koefficient = 1
    for line in lines_orig:
        if line['length_real'] is not None:
            id = line['id']
            line_num = find_element_by_id(id, lines_solved)
            koefficient = line['length_real'] / lines_solved[line_num]['length_real']
            break
        elif line['length_plan'] is not None:
            id = line['id']
            line_num = find_element_by_id(id, lines_solved)
            koefficient = line['length_plan'] / lines_solved[line_num]['length_plan']
            break

    return koefficient


def set_heights(shapes_orig, shapes):

    lines_orig = list(exact_lines(shapes_orig).values())
    lines_solved = list(exact_lines(shapes).values())

    koefficient = find_koefficient(lines_orig, lines_solved)

    for line in lines_orig:

        line_id = find_element_by_id(line['id'], lines_solved)
        line_solved = lines_solved[line_id]

        if line_solved['line_height'] is not None:
            if line['points'][0]['z'] is not None and line['points'][1]['z'] is None:
                line['points'][1]['z'] = line['points'][0]['z'] \
                        + line_solved['line_height'] * koefficient

            elif line['points'][1]['z'] is not None and line['points'][0]['z'] is None:
                line['points'][0]['z'] = line['points'][1]['z'] \
                        + line_solved['line_height'] * koefficient


    for shape in shapes:
        answer = []
        for line in shape['lines']:
            answer.append(lines_solved[
                find_element_by_id(line['id'], lines_solved)
            ])

        shape['lines'] = answer

    return shapes


def calc_real_length(shapes_orig, shapes_solved):

    lines_orig = list(exact_lines(shapes_orig).values())
    lines_solved = list(exact_lines(shapes_solved).values())

    koefficient = find_koefficient(lines_orig, lines_solved)

    if koefficient == 1:
        for shape in shapes_orig:
            if shape['square'] is not None:
                id = shape['id']
                shape_num = find_element_by_id(id, shapes_solved)
                koefficient = math.sqrt(shape['square'] / shapes_solved[shape_num]['square'])
                break


    for line in lines_orig:
        line_id = find_element_by_id(line['id'], lines_solved)
        line_solved = lines_solved[line_id]

        if line['length_plan'] is None and line_solved['length_plan'] is not None:
            line_solved['length_plan'] = line_solved['length_plan'] * koefficient
        if line['length_real'] is None and line_solved['length_real'] is not None:
            line_solved['length_real'] = line_solved['length_real'] * koefficient

        if line['angle'] is None:
            line['angle'] = line_solved['angle']


    # Set koefficient to calculate real shapes lengths
    koefficient = koefficient * koefficient

    for shape in shapes_solved:
        answer = []
        for line in shape['lines']:
            answer.append(lines_solved[
                find_element_by_id(line['id'], lines_solved)
            ])

        shape['lines'] = answer

        if shape['square'] is not None:
            shape['square'] *= koefficient

    return shapes_solved, koefficient


def exact_coords(lines):

    extracted_coords = {}

    for line in lines:
        for point in line['points']:
            id = point['id']
            if id not in extracted_coords.keys():
                extracted_coords[id] = point


    return extracted_coords


def exact_lines(shapes):

    extracted_lines = {}

    for shape in shapes:
        for line in shape['lines']:
            id = line['id']
            if id not in extracted_lines.keys():
                extracted_lines[id] = line
            else:
                if extracted_lines[id]['points'][0]['z'] is None:
                    extracted_lines[id]['points'][0]['z'] = line['points'][0]['z']
                if extracted_lines[id]['points'][1]['z'] is None:
                    extracted_lines[id]['points'][1]['z'] = line['points'][1]['z']
                if extracted_lines[id]['angle'] is None:
                    extracted_lines[id]['angle'] = line['angle']

    return extracted_lines


def exact_lines_from_single_shape(shape):

    extracted_lines = {}

    for line in shape['lines']:
        id = line['id']
        if id not in extracted_lines.keys():
            extracted_lines[id] = line

    return extracted_lines


def find_element_by_id(id, elements):

    i = 0
    for element in elements:
        if element['id'] == id:
            return i
        i += 1
