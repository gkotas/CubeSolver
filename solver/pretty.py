COLOR_TEXT = "\033[0;30;%dm  \033[0m"

RED = COLOR_TEXT % 41
BLUE = COLOR_TEXT % 44
GREEN = COLOR_TEXT % 42
WHITE = COLOR_TEXT % 47
YELLOW = COLOR_TEXT % 43
ORANGE = COLOR_TEXT % 45  # Purple since orange isn't an option

def prettyPrint(cube):
    '''
    Takes a cube and prints in color.
    '''
    layout = cube.getLayout()
    layout = layout.replace('R', RED)
    layout = layout.replace('B', BLUE)
    layout = layout.replace('G', GREEN)
    layout = layout.replace('W', WHITE)
    layout = layout.replace('Y', YELLOW)
    layout = layout.replace('O', ORANGE)

    layout = layout.replace('   ', '      ')

    print(layout)

if __name__ == '__main__':
    from cube import Cube
    cube = Cube('RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO')

    prettyPrint(cube)
