from constants import *

class Solver():
    def __init__(self, cube):
        '''
        Class that takes a cube and solves it.
        '''
        self.cube = cube
        self.moves = []

    def solve(self):
        '''
        Returns the solved cube.
        '''
        self._solveCross()

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

        print(df)
        print(dr)
        print(db)
        print(dl)

        ######################
        # Solve the df piece #
        ######################
        for piece in (df, dr, db, dl):
            print("\n\nSolving a new piece")
            print(piece)
            prettyPrint(self.cube)

            # Get the face of the down color
            down_color_face = piece.getCubieFaceFromColor(down_color)

            # Continue if piece is solved
            if all(piece.pos == DOWN + FRONT) and down_color_face == 'D':
                print("Piece is already solved")

            else:
                # Move to up layer, if not already
                if not piece.onFace(UP):
                    print("Need to Up layer")
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
                        # Need to rotate face, face, Up, face, face
                        self.moves.append(other_color_face)
                        self.moves.append(other_color_face)
                        self.moves.append('U')
                        self.moves.append(other_color_face)
                        self.moves.append(other_color_face)
                        self.cube.moveSequence(f'{other_color_face} {other_color_face} U {other_color_face} {other_color_face}')

                    else:
                        # OPTIMIZE: if down_color on down face, don't need to move to U layer first
                        print("ERROR: Uh oh")

                print("Peice on Up layer")
                prettyPrint(self.cube)

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
                        print("Need to spin to side")
                        self.moves.append('U')
                        self.cube.U()

                    # On either Left or Right
                    assert piece.onFace(LEFT) or piece.onFace(RIGHT)

                    self.moves.append('Mi')
                    self.cube.Mi()

                    if piece.onFace(LEFT):
                        print("On left face")
                        self.moves.append('Ui')
                        self.cube.Ui()
                    elif piece.onFace(RIGHT):
                        print("On right face")
                        self.moves.append('U')
                        self.cube.U()

                    self.moves.append('M')
                    self.cube.M()

            print("Peice solved")
            prettyPrint(self.cube)

            # Spin whole cube to handle next piece
            self.cube.Y()
            self.moves.append('Y')





if __name__ == '__main__':
    from cube import Cube
    from pretty import prettyPrint

    cube = Cube('RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO')
    cube.scramble()

    prettyPrint(cube)

    solver = Solver(cube)
    solver.solve()

    prettyPrint(cube)
