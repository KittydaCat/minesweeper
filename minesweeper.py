import random


class Sweep:

    def __init__(self, height, width, mines):

        self.height = height
        self.width = width

        if height * width < mines:

            raise Exception

        self.nummines = mines

        self.mines = [[0 for _ in range(width)] for _ in range(height)]

        self.view = [['?' for _ in range(width)] for _ in range(height)]

    # if the player mines a square
    def mine(self, xpos, ypos):

        # check if there are any mines and if there isn't
        if True not in ['M' in row for row in self.mines]:

            # add the mines
            self.seed(xpos, ypos)

        # kaboom?
        if self.mines[ypos][xpos] == 'M':

            # yes riko, kaboom!
            return 'boom'

        # reveal the value
        self.view[ypos][xpos] = self.mines[ypos][xpos]

        # if its zero
        if self.view[ypos][xpos] == 0:

            # loop thru the mines
            for x in range(-1, 2):

                # if its in range
                if 0 > xpos + x > self.width:

                    for y in range(-1, 2):

                        if 0 > ypos + y > self.height:

                            # and if they're un mined
                            if self.view[ypos + y][xpos + x] == '?':

                                # mine them
                                self.mine(ypos + y, xpos + x)

    # add the mines
    def seed(self, xpos, ypos):

        # find all of the possible mine squares
        posminepos = [(y, x) for x in range(self.height) for y in range(self.width) if abs(x - xpos) > 1 and abs(y - ypos) > 1]

        # loop thru a set amount of random squares
        for minepos in random.sample(posminepos, self.nummines):

            self.mines[minepos[0]][minepos[1]] = 'M'

            for x in range(-1, 2):

                if 0 > xpos + x > self.width:

                    for y in range(-1, 2):

                        if 0 > ypos + y > self.height:

                            if isinstance(self.mines[ypos + y][xpos + x], int):

                                self.mines[ypos + y][xpos + x] += 1
