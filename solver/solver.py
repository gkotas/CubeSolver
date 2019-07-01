from constants import *

class Solver():
    def __init__(self, cube, debug=False):
        '''
        Class that takes a cube and solves it.
        '''
        self.cube = cube
        self.moves = []
        self.debug = debug

    def solve(self):
        '''
        Returns the solved cube.
        '''
        self._solveCross()
        if self.debug:
            print("Solved Cross")
            prettyPrint(self.cube)

        self._solveFirstLayer()
        if self.debug:
            print("Solved First Layer")
            prettyPrint(self.cube)

        self._solveSecondLayer()
        if self.debug:
            print("Solved Second Layer")
            prettyPrint(self.cube)

        self._solveTopCross()
        if self.debug:
            print("Solved Top Cross")
            prettyPrint(self.cube)

        self._solveTopLayer()

        print(' '.join(self.moves))
        print(len(self.moves))

    def _solveCross(self):
        '''
        Step 1: Get the cross on the down face.
        '''
        df = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                         self.cube.getCubeFaceColor(FRONT)))
        dr = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                         self.cube.getCubeFaceColor(RIGHT)))
        db = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                         self.cube.getCubeFaceColor(BACK)))
        dl = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                         self.cube.getCubeFaceColor(LEFT)))

        down_color = self.cube.getCubeFaceColor(DOWN)

        ######################
        # Solve the df piece #
        ######################
        # OPTIMIZE: Try out other orders for a lower move possibility
        for piece in (df, dr, db, dl):
            # Get the face of the down color
            down_color_face = piece.getCubieFaceFromColor(down_color)

            # Continue if piece is solved
            if all(piece.pos == DOWN + FRONT) and down_color_face == 'D':
                # Piece is already solved
                pass

            else:
                # Move to up layer, if not already
                if not piece.onFace(UP):
                    # Get color of cubie that isn't the down color
                    other_color = (piece.getCubieColors() - set((down_color,))).pop()
                    # Get the face of the other color
                    other_color_face = piece.getCubieFaceFromColor(other_color)


                    # In E layer
                    if (other_color_face + down_color_face) in ('FL', 'RF', 'BR', 'LB'):
                        # Need to rotate face, UP, inverse face
                        self.moves.append(other_color_face)
                        self.moves.append('U')
                        self.moves.append(other_color_face + 'i')
                        self.cube.moveSequence(f'{other_color_face} U {other_color_face}i')

                    # Also in E layer
                    elif (other_color_face + down_color_face) in ('LF', 'FR', 'RB', 'BL'):
                        # Need to rotate inverse face, UP, face
                        self.moves.append(other_color_face + 'i')
                        self.moves.append('U')
                        self.moves.append(other_color_face)
                        self.cube.moveSequence(f'{other_color_face}i U {other_color_face}')

                    # In D layer
                    elif (other_color_face + down_color_face) in ('DF', 'DR', 'DB', 'DL'):
                        # Need to rotate face, face, Up, face, face
                        self.moves.append(down_color_face)
                        self.moves.append(down_color_face)
                        self.moves.append('U')
                        self.moves.append(down_color_face)
                        self.moves.append(down_color_face)
                        self.cube.moveSequence(f'{down_color_face} {down_color_face} U {down_color_face} {down_color_face}')

                    elif (other_color_face + down_color_face) in ('FD', 'RD', 'BD', 'LD'):
                        # OPTIMIZE: if down_color on down face, don't need to move to U layer first
                        # Need to rotate face, face, Up, face, face
                        self.moves.append(other_color_face)
                        self.moves.append(other_color_face)
                        self.moves.append('U')
                        self.moves.append(other_color_face)
                        self.moves.append(other_color_face)
                        self.cube.moveSequence(f'{other_color_face} {other_color_face} U {other_color_face} {other_color_face}')

                    else:
                        assert False, "Piece wasn't in a spot to move to U layer"

                # If Down color is on Up face, rotate Up until on correct face and spin
                # face twice
                if piece.getCubieFaceColor(UP) == cube.getCubeFaceColor(DOWN):
                    # In up layer, to Up+Front
                    count = 0
                    while not all(piece.pos == UP + FRONT):
                        count += 1
                        self.moves.append('U')
                        self.cube.U()
                        assert count < 4, "Piece can't get to UP+FRONT"

                    # Piece is above, two front turns
                    self.moves.append('F')
                    self.moves.append('F')
                    self.cube.F()
                    self.cube.F()

                # Down color is not on Up face, move to either Left or Right face
                else:
                    # Need to put it to the right or left side if not already
                    if piece.onFace(FRONT) or piece.onFace(BACK):
                        self.moves.append('U')
                        self.cube.U()

                    # On either Left or Right
                    assert piece.onFace(LEFT) or piece.onFace(RIGHT)

                    self.moves.append('Mi')
                    self.cube.Mi()

                    if piece.onFace(LEFT):
                        self.moves.append('Ui')
                        self.cube.Ui()
                    elif piece.onFace(RIGHT):
                        self.moves.append('U')
                        self.cube.U()

                    self.moves.append('M')
                    self.cube.M()

            # Spin whole cube to handle next piece
            self.cube.Y()
            self.moves.append('Y')

    def _solveFirstLayer(self):
        '''
        Step 2: Put in the corners on the down face.
        '''
        dfr = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                          self.cube.getCubeFaceColor(FRONT),
                                          self.cube.getCubeFaceColor(RIGHT)))
        drb = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                          self.cube.getCubeFaceColor(RIGHT),
                                          self.cube.getCubeFaceColor(BACK)))
        dbl = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                          self.cube.getCubeFaceColor(BACK),
                                          self.cube.getCubeFaceColor(LEFT)))
        dlf = self.cube.getCubieByColors((self.cube.getCubeFaceColor(DOWN),
                                          self.cube.getCubeFaceColor(LEFT),
                                          self.cube.getCubeFaceColor(FRONT)))

        down_color = self.cube.getCubeFaceColor(DOWN)

        # OPTIMIZE: Do a better order
        for piece in (dfr, drb, dbl, dlf):
            # Get the face of the down color
            down_color_face = piece.getCubieFaceFromColor(down_color)

            # Continue if piece is solved
            if all(piece.pos == DOWN + FRONT + RIGHT) and down_color_face == 'D':
                # Piece is already solved
                pass

            else:
                # Move piece to U layer if not already
                if not piece.onFace(UP):
                    # Spin cube until piece is in DFR
                    count = 0
                    while not all(piece.pos == DOWN + FRONT + RIGHT):
                        count += 1
                        self.cube.Y()
                        self.moves.append('Y')
                        assert count < 4, "Piece can't get to DOWN+FRONT+RIGHT"

                    # Update the face of the down color since cube may have spun
                    down_color_face = piece.getCubieFaceFromColor(down_color)

                    if down_color_face == 'F':
                        self.moves.append('Fi')
                        self.moves.append('Ui')
                        self.moves.append('F')
                        self.cube.Fi()
                        self.cube.Ui()
                        self.cube.F()
                    elif down_color_face in ('R', 'D'):
                        self.moves.append('R')
                        self.moves.append('U')
                        self.moves.append('Ri')
                        self.cube.R()
                        self.cube.U()
                        self.cube.Ri()
                    else:
                        assert False, "Down color isn't on F, R, or D?"

                    # Return cube back to original orientation
                    for _ in range(count):
                        self.cube.Yi()
                        self.moves.append('Yi')



                elif down_color_face == 'U':
                    # Piece is on U layer, but down color is on U face
                    # Rotate UP until peice is at UFR
                    count = 0
                    while not all(piece.pos == UP + FRONT + RIGHT):
                        count += 1
                        self.cube.U()
                        self.moves.append('U')
                        assert count < 4, "Piece can't get to UP+FRONT+RIGHT"

                    self.cube.R()
                    self.cube.Ui()
                    self.cube.Ri()
                    self.moves.append('R')
                    self.moves.append('Ui')
                    self.moves.append('Ri')

                # Update the face of the down color since piece may have moved
                down_color_face = piece.getCubieFaceFromColor(down_color)

                # Piece should be on UP face with the down color not on UP face
                assert piece.onFace(UP) and down_color_face != 'U'

                # Color on UP determines if F or R is used to drop into DFR
                up_face_color = piece.getCubieFaceColor(UP)

                if up_face_color == self.cube.getCubeFaceColor(RIGHT):
                    # Piece must be moved to UBR
                    count = 0
                    while not all(piece.pos == UP + BACK + RIGHT):
                        count += 1
                        self.cube.U()
                        self.moves.append('U')
                        assert count < 4, "Piece can't get to UP+BACK+RIGHT"

                    self.cube.Fi()
                    self.cube.U()
                    self.cube.F()
                    self.moves.append('Fi')
                    self.moves.append('U')
                    self.moves.append('F')

                elif up_face_color == self.cube.getCubeFaceColor(FRONT):
                    # Piece must be moved to UFL
                    count = 0
                    while not all(piece.pos == UP + FRONT + LEFT):
                        count += 1
                        self.cube.U()
                        self.moves.append('U')
                        assert count < 4, "Piece can't get to UP+FRONT+LEFT"

                    self.cube.R()
                    self.cube.Ui()
                    self.cube.Ri()
                    self.moves.append('R')
                    self.moves.append('Ui')
                    self.moves.append('Ri')
                else:
                    assert False, "up_face_color isn't F or R?"

            # Spin whole cube to handle next piece
            self.cube.Y()
            self.moves.append('Y')

    def _solveSecondLayer(self):
        '''
        Step 3: Put in the edges on the second layer.
        '''
        fr = self.cube.getCubieByColors((self.cube.getCubeFaceColor(FRONT),
                                         self.cube.getCubeFaceColor(RIGHT)))
        rb = self.cube.getCubieByColors((self.cube.getCubeFaceColor(RIGHT),
                                         self.cube.getCubeFaceColor(BACK)))
        bl = self.cube.getCubieByColors((self.cube.getCubeFaceColor(BACK),
                                         self.cube.getCubeFaceColor(LEFT)))
        lf = self.cube.getCubieByColors((self.cube.getCubeFaceColor(LEFT),
                                         self.cube.getCubeFaceColor(FRONT)))

        # OPTIMIZE: Try out other orders for a lower move possibility
        for piece in (fr, rb, bl, lf):
            # Get the face of the front color
            front_color = self.cube.getCubeFaceColor(FRONT)
            front_color_face = piece.getCubieFaceFromColor(front_color)

            if all(piece.pos == FRONT + RIGHT):
                # Continue if piece is solved
                if front_color_face == 'F':
                    # Piece is already solved
                    pass
                else:
                    # Piece needs to be flipped
                    seq = 'R Ui Ri U Fi U U F U U Fi U F'
                    self.cube.moveSequence(seq)
                    self.moves.extend(seq.split(' '))
            else:
                # Move piece to U layer if not already
                if not piece.onFace(UP):
                    # Spin cube until piece is in FRONT + RIGHT
                    count = 0
                    while not all(piece.pos == FRONT + RIGHT):
                        count += 1
                        self.cube.Y()
                        self.moves.append('Y')
                        assert count < 4, "Piece can't get to DOWN+FRONT+RIGHT"

                    prettyPrint(self.cube)
                    seq = 'R Ui Ri Ui Fi U F'
                    self.cube.moveSequence(seq)
                    self.moves.extend(seq.split(' '))

                    # Return cube back to original orientation
                    for _ in range(count):
                        self.cube.Yi()
                        self.moves.append('Yi')

                # Color on UP determines if F or R is used to drop into DFR
                up_face_color = piece.getCubieFaceColor(UP)

                if up_face_color == self.cube.getCubeFaceColor(RIGHT):
                    # Piece must be moved to UL
                    count = 0
                    while not all(piece.pos == UP + LEFT):
                        count += 1
                        self.cube.U()
                        self.moves.append('U')
                        assert count < 4, "Piece can't get to UP+LEFT"

                    seq = 'R Ui Ri Ui Fi U F'
                    self.cube.moveSequence(seq)
                    self.moves.extend(seq.split(' '))

                elif up_face_color == self.cube.getCubeFaceColor(FRONT):
                    # Piece must be moved to UB
                    count = 0
                    while not all(piece.pos == UP + BACK):
                        count += 1
                        self.cube.U()
                        self.moves.append('U')
                        assert count < 4, "Piece can't get to UP+BACK"

                    seq = 'Fi U F U R Ui Ri'
                    self.cube.moveSequence(seq)
                    self.moves.extend(seq.split(' '))
                else:
                    assert False, "up_face_color isn't F or R?"

            # Spin whole cube to handle next piece
            self.cube.Y()
            self.moves.append('Y')

    def _solveTopCross(self):
        '''
        Step 4: Solve the edges on the top layer to make the cross.
        '''
        uf = self.cube.getCubieByPosition(UP + FRONT)
        ur = self.cube.getCubieByPosition(UP + RIGHT)
        ub = self.cube.getCubieByPosition(UP + BACK)
        ul = self.cube.getCubieByPosition(UP + LEFT)

        up_color = self.cube.getCubeFaceColor(UP)

        correct_pieces = [
            uf.getCubieFaceColor(UP) == up_color,
            ur.getCubieFaceColor(UP) == up_color,
            ub.getCubieFaceColor(UP) == up_color,
            ul.getCubieFaceColor(UP) == up_color,
        ]

        if correct_pieces == [True, True, True, True]:
            # Cross is solved
            pass
        elif correct_pieces == [False, False, False, False]:
            # No pieces in cross
            seq = 'F R U Ri Ui S R U Ri Ui Bi Zi'
            self.cube.moveSequence(seq)
            self.moves.extend(seq.split(' '))
        elif correct_pieces == [False, True, False, True]:
            # I shape from Right to Left
            seq = 'F R U Ri Ui Fi'
            self.cube.moveSequence(seq)
            self.moves.extend(seq.split(' '))
        elif correct_pieces == [True, False, True, False]:
            # I shape from Right to Left
            seq = 'Y F R U Ri Ui Fi'
            self.cube.moveSequence(seq)
            self.moves.extend(seq.split(' '))
        else:
            # Must be L in 1 of 4 positions, Spin so its Front Right
            count = 0
            while correct_pieces != [True, True, False, False]:
                count += 1
                self.cube.Y()
                self.moves.append('Y')
                correct_pieces = correct_pieces[1:] + [correct_pieces[0]]
                assert count < 4, "Piece can't get to DOWN+FRONT+RIGHT"

            seq = 'B Z R U Ri Ui Bi Zi'
            self.cube.moveSequence(seq)
            self.moves.extend(seq.split(' '))

    def _solveTopLayer(self):
        '''
        Step 4: Solve the corners to solve the top face.
        '''
        ufr = self.cube.getCubieByPosition(UP + FRONT + RIGHT)
        urb = self.cube.getCubieByPosition(UP + RIGHT + BACK)
        ubl = self.cube.getCubieByPosition(UP + BACK + LEFT)
        ulf = self.cube.getCubieByPosition(UP + LEFT + FRONT)

        up_color = self.cube.getCubeFaceColor(UP)

        clockwise_solves = [0, 0, 0, 0]

        if ufr.getCubieFaceFromColor(up_color) == 'F':
            clockwise_solves[0] = 1
        elif ufr.getCubieFaceFromColor(up_color) == 'R':
            clockwise_solves[0] = 2

        if urb.getCubieFaceFromColor(up_color) == 'R':
            clockwise_solves[1] = 1
        elif urb.getCubieFaceFromColor(up_color) == 'B':
            clockwise_solves[1] = 2

        if ubl.getCubieFaceFromColor(up_color) == 'B':
            clockwise_solves[2] = 1
        elif ubl.getCubieFaceFromColor(up_color) == 'L':
            clockwise_solves[2] = 2

        if ulf.getCubieFaceFromColor(up_color) == 'L':
            clockwise_solves[3] = 1
        elif ulf.getCubieFaceFromColor(up_color) == 'F':
            clockwise_solves[3] = 2

        print(clockwise_solves)

        count = 0
        while count < 4:
            if clockwise_solves == [0, 0, 0, 0]:
                #
                #   |X|X|X|
                #   |X|X|X|  -> [0, 0, 0, 0]
                #   |X|X|X|
                #
                return

            if clockwise_solves == [1, 2, 2, 1]:
                #        X
                #  X| |X| |
                #   |X|X|X|  -> [1, 2, 2, 1]
                #  X| |X| |
                #        X
                seq = 'R U U R R Ui R R Ui R R U U R'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [1, 1, 1, 0]:
                #    X
                #   | |X| |X
                #   |X|X|X|  -> [1, 1, 1, 0]
                #   |X|X| |
                #        X
                seq = 'R Ui Li U Ri Ui L'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [0, 2, 2, 2]:
                #        X
                #  X| |X| |
                #   |X|X|X|  -> [0, 2, 2, 2]
                #   | |X|X|
                #    X
                seq = 'Li U R Ui L U Ri'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [1, 2, 1, 2]:
                #    X   X
                #   | |X| |
                #   |X|X|X|  -> [1, 2, 1, 2]
                #   | |X| |
                #    X   X
                seq = 'F R U Ri Ui R U Ri Ui R U Ri Ui Fi'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [0, 0, 1, 2]:
                #    X
                #   | |X|X|
                #   |X|X|X|  -> [0, 0, 1, 2]
                #   | |X|X|
                #    X
                seq = 'L X U Ri Ui Li Xi F R Fi'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [1, 0, 2, 0]:
                #
                #  X| |X|X|
                #   |X|X|X|  -> [1, 0, 2, 0]
                #   |X|X| |
                #        X
                seq = 'Fi L X U Ri Ui Li Xi F R'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            if clockwise_solves == [0, 0, 2, 1]:
                #
                #  X| |X|X|
                #   |X|X|X|  -> [0, 0, 2, 1]
                #  X| |X|X|
                #
                print("Superman")
                seq = 'R U Ri Ui R Ui Ri U U R Ui Ri U U R U Ri'
                self.cube.moveSequence(seq)
                self.moves.extend(seq.split(' '))
                return

            # Not a match to a known state, spin cube and check again
            count += 1
            self.cube.Y()
            self.moves.append('Y')
            clockwise_solves = clockwise_solves[1:] + clockwise_solves[:1]

        # Spin cube 4 times and couldn't match
        print(clockwise_solves)
        assert False, "No match to solve top layer."


if __name__ == '__main__':
    from cube import Cube
    from pretty import prettyPrint

    for i in range(50):
        cube = Cube('RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO')
        cube.scramble(i)

        prettyPrint(cube)

        solver = Solver(cube, True)
        solver.solve()

        prettyPrint(cube)

        print("Seed:", i)
        input()
