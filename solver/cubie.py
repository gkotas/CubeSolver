import numpy as np

from constants import RIGHT, LEFT, FRONT, BACK, UP, DOWN


class Cubie():
    def __init__(self, pos, colors):
        '''
        Class for each cubie of the cube.
            pos: numpy 3-tuple for x-y-z integer coordinates in range (-1, 1)
            colors: 3-tuple of colors in the corresponding x-y-z directions

            +x is right face, -x is left face
            +y is up face,    -y is down face
            +z is front face, -z is back face
        '''
        self.pos = pos
        self.colors = colors

    def __repr__(self):
        return f'Cubie: {self.pos.transpose()}, {self.colors}'

    # Get Coordinates
    def x(self): return self.pos[0]
    def y(self): return self.pos[1]
    def z(self): return self.pos[2]

    def rotate(self, rotation_matrix):
        '''
        Applies the rotation_matrix to this cubie.
        '''
        self.pos = np.matmul(rotation_matrix, self.pos)

        new_colors = [None] * 3
        for i, j in np.transpose(rotation_matrix.nonzero()):
            new_colors[i] = self.colors[j]
        self.colors = new_colors

    def getCubieFaceColor(self, face):
        '''
        Returns the color of the cubie on the specified face.
        '''
        # Uses index of nonzero element of the face to get the color
        return self.colors[int(face.nonzero()[0])]

    def getCubieColors(self):
        '''
        Returns a set of the colors of the cubie.
        '''
        return set(c for c in self.colors if c != None)

    def onFace(self, face):
        '''
        Returns true if the cubie is on the specified face.
        '''
        return np.dot(face.squeeze(), self.pos.squeeze()) == 1

    def getCubieFaceFromColor(self, color):
        '''
        Returns the face of the cube that has the specified color.
        '''
        # Either Right or Left
        if self.colors[0] == color:
            if self.x() == 1:
                return 'R'
            elif self.x() == -1:
                return 'L'

        # Either Up or Down
        if self.colors[1] == color:
            if self.y() == 1:
                return 'U'
            elif self.y() == -1:
                return 'D'

        # Either Front or Back
        if self.colors[2] == color:
            if self.z() == 1:
                return 'F'
            elif self.z() == -1:
                return 'B'


    def inSlice(self, slice):
        '''
        Returns true if the cubie is in the specified slice.
        '''
        return np.dot(slice.squeeze(), self.pos.squeeze()) == 0
