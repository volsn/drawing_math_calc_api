def exact_coords(lines):

    coords = []
    for line in lines:
        for point in line['points']:
            x = line['points']['x']
            y = line['points']['y']
            coords.append(tuple([x, y]))
    return coords
