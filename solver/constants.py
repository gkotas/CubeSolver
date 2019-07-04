import numpy as np


# Faces
RIGHT = np.array([[ 1], [ 0], [ 0]])
LEFT  = np.array([[-1], [ 0], [ 0]])
UP    = np.array([[ 0], [ 1], [ 0]])
DOWN  = np.array([[ 0], [-1], [ 0]])
FRONT = np.array([[ 0], [ 0], [ 1]])
BACK  = np.array([[ 0], [ 0], [-1]])

# Slices
MIDDLE     = LEFT
EQUATORIAL = DOWN
STANDING   = FRONT

# Colors
RED = 'R'
WHITE = 'W'
BLUE = 'B'
GREEN = 'G'
ORANGE = 'O'
YELLOW = 'Y'

# Rotation Matrices
XY_CW = np.array([[ 0, 1, 0],
                  [-1, 0, 0],
                  [ 0, 0, 1]])
XY_CCW = XY_CW.transpose()

YZ_CW = np.array([[1,  0, 0],
                  [0,  0, 1],
                  [0, -1, 0]])
YZ_CCW = YZ_CW.transpose()

XZ_CW = np.array([[0, 0, -1],
                  [0, 1,  0],
                  [1, 0,  0]])
XZ_CCW = XZ_CW.transpose()


# Cube Spin Translations
TRANSLATIONS = {
    'X': {
        'L': 'L',
        'Li': 'Li',
        'R': 'R',
        'Ri': 'Ri',
        'M': 'M',
        'Mi': 'Mi',

        'U': 'F',
        'Ui': 'Fi',
        'D': 'B',
        'Di': 'Bi',
        'E': 'S',
        'Ei': 'Si',

        'F': 'D',
        'Fi': 'Di',
        'B': 'U',
        'Bi': 'Ui',
        'S': 'E',
        'Si': 'Ei',
    },
    'Xi': {
        'L': 'L',
        'Li': 'Li',
        'R': 'R',
        'Ri': 'Ri',
        'M': 'M',
        'Mi': 'Mi',

        'U': 'B',
        'Ui': 'Bi',
        'D': 'F',
        'Di': 'Fi',
        'E': 'S',
        'Ei': 'Si',

        'F': 'U',
        'Fi': 'Ui',
        'B': 'D',
        'Bi': 'Di',
        'S': 'E',
        'Si': 'Ei',
    },
    'Y': {
        'L': 'F',
        'Li': 'Fi',
        'R': 'B',
        'Ri': 'Bi',
        'M': 'S',
        'Mi': 'Si',

        'U': 'U',
        'Ui': 'Ui',
        'D': 'D',
        'Di': 'Di',
        'E': 'E',
        'Ei': 'Ei',

        'F': 'R',
        'Fi': 'Ri',
        'B': 'L',
        'Bi': 'Li',
        'S': 'M',
        'Si': 'Mi',
    },
    'Yi': {
        'L': 'B',
        'Li': 'Bi',
        'R': 'F',
        'Ri': 'Fi',
        'M': 'S',
        'Mi': 'Si',

        'U': 'U',
        'Ui': 'Ui',
        'D': 'D',
        'Di': 'Di',
        'E': 'E',
        'Ei': 'Ei',

        'F': 'L',
        'Fi': 'Li',
        'B': 'R',
        'Bi': 'Ri',
        'S': 'M',
        'Si': 'Mi',
    },
    'Z': {
        'L': 'D',
        'Li': 'Di',
        'R': 'U',
        'Ri': 'Ui',
        'M': 'E',
        'Mi': 'Ei',

        'U': 'L',
        'Ui': 'Li',
        'D': 'R',
        'Di': 'Ri',
        'E': 'M',
        'Ei': 'Mi',

        'F': 'F',
        'Fi': 'Fi',
        'B': 'B',
        'Bi': 'Bi',
        'S': 'S',
        'Si': 'Si',
    },
    'Zi': {
        'L': 'U',
        'Li': 'Ui',
        'R': 'D',
        'Ri': 'Di',
        'M': 'E',
        'Mi': 'Ei',

        'U': 'R',
        'Ui': 'Ri',
        'D': 'L',
        'Di': 'Li',
        'E': 'M',
        'Ei': 'Mi',

        'F': 'F',
        'Fi': 'Fi',
        'B': 'B',
        'Bi': 'Bi',
        'S': 'S',
        'Si': 'Si',
    },
}
