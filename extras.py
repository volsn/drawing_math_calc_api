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
