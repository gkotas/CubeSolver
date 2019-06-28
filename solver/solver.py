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

if __name__ == '__main__':
    from cube import Cube
    from pretty import prettyPrint

    cube = Cube('RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO')
    cube.scramble(42)

    prettyPrint(cube)

    solver = Solver(cube, True)
    solver.solve()

    prettyPrint(cube)

    # print("Seed:", i)
    # input()
