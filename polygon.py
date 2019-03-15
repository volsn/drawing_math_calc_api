import sys


def polygon_square(coords, absoluteValue=True):
    nbCoordinates = len(coords)
    nbSegment = nbCoordinates - 1

    l = [(coords[i+1][0] - coords[i][0]) * (coords[i+1][1] + coords[i][1]) for i in range(nbSegment)]

    if absoluteValue:
        return abs(sum(l) / 2.)
    else:
        return sum(l) / 2.

"""
For test purpose
"""
if __name__ == '__main__':

    coords = []
    for _ in range(int(sys.argv[1])):
        x = float(input())
        y = float(input())
        coords.append(tuple([x, y]))
    print(polygon_square(coords))
