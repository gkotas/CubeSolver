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
