import random
import tkinter as tk
from functools import partial


class Sweep:

    def __init__(self, height, width, mines):

        self.height = height
        self.width = width

        if height * width < mines:

            raise Exception

        self.nummines = mines

        # a queue for clearing the zeros
        self.queue = []

        # a pure view of the mines
        self.mines = [[0 for _ in range(width)] for _ in range(height)]

        # what the player sees
        self.view = [['?' for _ in range(width)] for _ in range(height)]

        # the tk display
        self.display = tk.Tk()

    # if the player mines a square
    def mine(self, xpos, ypos, recurved=False):

        print(xpos, ypos)

        # check if there are any mines and if there isn't
        if True not in ['M' in row for row in self.mines]:

            # add the mines
            self.seed(xpos, ypos)

        if self.view[ypos][xpos] == 'F':

            return

        # kaboom?
        if self.mines[ypos][xpos] == 'M':

            # yes riko, kaboom!
            return 'boom'

        # reveal the value
        self.view[ypos][xpos] = self.mines[ypos][xpos]

        # if its zero
        if self.view[ypos][xpos] == '0':

            # loop thru the squares
            for x in range(-1, 2):

                # if its in range
                if -1 < xpos + x < self.width:

                    for y in range(-1, 2):

                        if -1 < ypos + y < self.height:

                            # and if they're un mined
                            if self.view[ypos + y][xpos + x] == '?' and (ypos+y, xpos+x) not in self.queue:

                                # add them to the queue
                                print(ypos+y, xpos+x, sep=' ')
                                self.queue.append((ypos + y, xpos + x))

            # if this function is not recurved
            if not recurved:

                print(self.queue)

                # while there is a queue
                while len(self.queue) > 0:

                    # mine the queued block
                    self.mine(self.queue[-1][0], self.queue[-1][1], recurved=True)

                    # and remove it from the queue
                    self.queue.pop(-1)

    # flag a mine
    def flag(self, xpos, ypos, event):

        self.view[ypos][xpos] = 'F'

    # add the mines
    def seed(self, xpos, ypos):

        # find all of the possible mine squares
        posminepos = [(y, x) for x in range(self.height) for y in range(self.width) if abs(x-xpos) > 1 and abs(y-ypos) > 1]

        # loop thru a set amount of random squares
        for minepos in random.sample(posminepos, self.nummines):

            self.mines[minepos[0]][minepos[1]] = 'M'

            for x in range(-1, 2):

                if -1 < minepos[1] + x < self.width:

                    for y in range(-1, 2):

                        if -1 < minepos[0] + y < self.height:

                            if isinstance(self.mines[minepos[0] + y][minepos[1] + x], int):

                                self.mines[minepos[0] + y][minepos[1] + x] += 1

    def update_display(self):

        for r in range(self.height):

            for c in range(self.width):

                button = tk.Button(self.display, text=self.view[r][c], command=partial(self.mine, r, c))

                func = partial(self.flag, c, r)

                button.bind('<Button-3>', func)

                button.grid(row=r, column=c)

    def displaymines(self):

        for f in self.mines:

            for g in f:

                print(g, end='')

            print('')


if __name__ == '__main__':

    s = Sweep(5, 5, 5)
    s.mine(0, 0)
    s.update_display()
