import numpy as np
import random

from constants import *
from cubie import Cubie


class Cube():
    def __init__(self, colors):
        '''
        Class representation of a Rubik's Cube.
        '''
        if isinstance(colors, Cube):
            colors = colors.getColorString()
        self._createCubies(colors.upper())

    def getColorString(self):
        '''
        Return a string of the colors.
        '''
        u = sorted(self._getCubiesOnFace(UP), key=lambda c: [c.z(), c.x()])
        l = sorted(self._getCubiesOnFace(LEFT), key=lambda c: [-c.y(), c.z()])
        f = sorted(self._getCubiesOnFace(FRONT), key=lambda c: [-c.y(), c.x()])
        r = sorted(self._getCubiesOnFace(RIGHT), key=lambda c: [-c.y(), -c.z()])
        b = sorted(self._getCubiesOnFace(BACK), key=lambda c: [-c.y(), -c.x()])
        d = sorted(self._getCubiesOnFace(DOWN), key=lambda c: [-c.z(), c.x()])

        u = [c.getCubieFaceColor(UP) for c in u]
        l = [c.getCubieFaceColor(LEFT) for c in l]
        f = [c.getCubieFaceColor(FRONT) for c in f]
        r = [c.getCubieFaceColor(RIGHT) for c in r]
        b = [c.getCubieFaceColor(BACK) for c in b]
        d = [c.getCubieFaceColor(DOWN) for c in d]

        return ''.join(u + l + f + r + b + d)

    def getLayout(self):
        '''
        Returns the layout of the cube.
        '''
        return '''\
    {0}{1}{2}
    {3}{4}{5}
    {6}{7}{8}
{9}{10}{11} {18}{19}{20} {27}{28}{29} {36}{37}{38}
{12}{13}{14} {21}{22}{23} {30}{31}{32} {39}{40}{41}
{15}{16}{17} {24}{25}{26} {33}{34}{35} {42}{43}{44}
    {45}{46}{47}
    {48}{49}{50}
    {51}{52}{53}\n'''.format(*[c for c in self.getColorString()])

    def _createCubies(self, colors):
        '''
        Creates a cube from the color string in the format:
                   ----------
                   |00|01|02|
                   ----------
                   |03|04|05|
                   ----------
                   |06|07|08|
                   ----------
        ---------- ---------- ---------- ----------
        |09|10|11| |18|19|20| |27|28|29| |36|37|38|
        ---------- ---------- ---------- ----------
        |12|13|14| |21|22|23| |30|31|32| |39|40|41|
        ---------- ---------- ---------- ----------
        |15|16|17| |24|25|26| |33|34|35| |42|43|44|
        ---------- ---------- ---------- ----------
                   ----------
                   |45|46|47|
                   ----------
                   |48|49|50|
                   ----------
                   |51|52|53|
                   ----------
        '''
        assert len(colors) == 54, "Invalid Color String Length"
        self._cubies = [
            # Faces
            Cubie((RIGHT), (colors[31], None, None)),
            Cubie((LEFT),  (colors[13], None, None)),
            Cubie((UP),    (None, colors[ 4], None)),
            Cubie((DOWN),  (None, colors[49], None)),
            Cubie((FRONT), (None, None, colors[22])),
            Cubie((BACK),  (None, None, colors[40])),

            # Edges
            Cubie((RIGHT + UP),    (colors[28], colors[ 5], None)),
            Cubie((RIGHT + DOWN),  (colors[34], colors[50], None)),
            Cubie((LEFT + UP),     (colors[10], colors[ 3], None)),
            Cubie((LEFT + DOWN),   (colors[16], colors[48], None)),
            Cubie((RIGHT + FRONT), (colors[30], None, colors[23])),
            Cubie((LEFT + FRONT),  (colors[14], None, colors[21])),
            Cubie((RIGHT + BACK),  (colors[32], None, colors[39])),
            Cubie((LEFT + BACK),   (colors[12], None, colors[41])),
            Cubie((UP + FRONT),    (None, colors[ 7], colors[19])),
            Cubie((UP + BACK),     (None, colors[ 1], colors[37])),
            Cubie((DOWN + FRONT),  (None, colors[46], colors[25])),
            Cubie((DOWN + BACK),   (None, colors[52], colors[43])),

            # Corners
            Cubie((RIGHT + UP + FRONT),   (colors[27], colors[ 8], colors[20])),
            Cubie((LEFT + UP + FRONT),    (colors[11], colors[ 6], colors[18])),
            Cubie((RIGHT + DOWN + FRONT), (colors[33], colors[47], colors[26])),
            Cubie((LEFT + DOWN + FRONT),  (colors[17], colors[45], colors[24])),
            Cubie((RIGHT + UP + BACK),    (colors[29], colors[ 2], colors[36])),
            Cubie((LEFT + UP + BACK),     (colors[ 9], colors[ 0], colors[38])),
            Cubie((RIGHT + DOWN + BACK),  (colors[35], colors[53], colors[42])),
            Cubie((LEFT + DOWN + BACK),   (colors[15], colors[51], colors[44])),
        ]

        # Check all pieces exist by searching for colors
        # Faces
        assert self.getCubieByColors((RED)) != None, "Missing Piece"
        assert self.getCubieByColors((WHITE)) != None, "Missing Piece"
        assert self.getCubieByColors((BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE)) != None, "Missing Piece"
        assert self.getCubieByColors((YELLOW)) != None, "Missing Piece"

        # Edges
        assert self.getCubieByColors((RED, WHITE)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, YELLOW)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, WHITE)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, YELLOW)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((YELLOW, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((YELLOW, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((WHITE, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((WHITE, BLUE)) != None, "Missing Piece"

        # Corners
        assert self.getCubieByColors((RED, WHITE, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, WHITE, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, YELLOW, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((RED, YELLOW, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, WHITE, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, WHITE, GREEN)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, YELLOW, BLUE)) != None, "Missing Piece"
        assert self.getCubieByColors((ORANGE, YELLOW, GREEN)) != None, "Missing Piece"


    def getCubieByColors(self, colors):
        '''
        Searches list of cubies for one matching the colors specified. Returns
        found cubie or None if not found.
        '''
        for cubie in self._cubies:
            if set(colors) == cubie.getCubieColors():
                return cubie

        # Not found
        return None

    def getCubieByPosition(self, pos):
        '''
        Returns the cubie in the specified position.
        '''
        for cubie in self._cubies:
            if all(cubie.pos == pos):
                return cubie

    # Face Rotation Functions
    def R(self): self._rotateFace(RIGHT, YZ_CW)
    def Ri(self): self._rotateFace(RIGHT, YZ_CCW)
    def L(self): self._rotateFace(LEFT, YZ_CCW)
    def Li(self): self._rotateFace(LEFT, YZ_CW)
    def U(self): self._rotateFace(UP, XZ_CW)
    def Ui(self): self._rotateFace(UP, XZ_CCW)
    def D(self): self._rotateFace(DOWN, XZ_CCW)
    def Di(self): self._rotateFace(DOWN, XZ_CW)
    def F(self): self._rotateFace(FRONT, XY_CW)
    def Fi(self): self._rotateFace(FRONT, XY_CCW)
    def B(self): self._rotateFace(BACK, XY_CCW)
    def Bi(self): self._rotateFace(BACK, XY_CW)

    # Slice Rotation Functions
    def M(self): self._rotateSlice(MIDDLE, YZ_CCW)
    def Mi(self): self._rotateSlice(MIDDLE, YZ_CW)
    def E(self): self._rotateSlice(EQUATORIAL, XZ_CCW)
    def Ei(self): self._rotateSlice(EQUATORIAL, XZ_CW)
    def S(self): self._rotateSlice(STANDING, XY_CW)
    def Si(self): self._rotateSlice(STANDING, XY_CCW)

    # Cube Rotation Functions
    def X(self): self._rotateCube(YZ_CW)
    def Xi(self): self._rotateCube(YZ_CCW)
    def Y(self): self._rotateCube(XZ_CW)
    def Yi(self): self._rotateCube(XZ_CCW)
    def Z(self): self._rotateCube(XY_CW)
    def Zi(self): self._rotateCube(XY_CCW)

    def moveSequence(self, seq):
        '''
        Takes a string of moves, space delimited, and applies the moves.
        '''
        moves = seq.split(' ')
        for move in moves:
            getattr(self, move)()

    def scramble(self, seed=None):
        '''
        Applies a set of random moves to the cube and returns the move sequence.
        '''
        valid_moves = ['R', 'L', 'U', 'D', 'F', 'B']
        # Add the inverses to the list
        valid_moves += [move + 'i' for move in valid_moves]

        if seed:
            random.seed(seed)

        # Pick 30 random moves
        moves = []
        for _ in range(30):
            moves.append(random.choice(valid_moves))

        # Make sequence string
        sequence = ' '.join(moves)
        self.moveSequence(sequence)

        return sequence

    def _rotateFace(self, face, rotation_matrix):
        '''
        Rotates each cubie on the face.
        '''
        for c in self._getCubiesOnFace(face):
            c.rotate(rotation_matrix)

    def _rotateSlice(self, slice, rotation_matrix):
        '''
        Rotates each cubie in the slice.
        '''
        for c in self._getCubiesInSlice(slice):
            c.rotate(rotation_matrix)

    def _rotateCube(self, rotation_matrix):
        '''
        Rotates each cubie.
        '''
        for c in self._cubies:
            c.rotate(rotation_matrix)

    def _getCubiesOnFace(self, face):
        '''
        Returns a list of cubies on the specified face.
        '''
        return [c for c in self._cubies if c.onFace(face)]

    def _getCubiesInSlice(self, slice):
        '''
        Returns a list of cubies in the specified slice.
        '''
        return [c for c in self._cubies if c.inSlice(slice)]

    def getCubeFaceColor(self, face):
        '''
        Returns the color of the face of the cube.
        '''
        return self.getCubieByPosition(face).getCubieFaceColor(face)

if __name__ == '__main__':
    from pretty import prettyPrint

    cube = Cube('RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO')

    prettyPrint(cube)

    # cube.R()
    print(cube.scramble(42))

    prettyPrint(cube)
