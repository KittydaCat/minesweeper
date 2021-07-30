import random
import tkinter as tk
from functools import partial
import time


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

    # returns the amount of unmined neighbors
    def unmined_neighbors(self, cords):

        lis = self.value_neighbors(cords)

        return lis.count('?') + lis.count('F')

    # returns the value of the neighbors for a position
    def value_neighbors(self, cords):

        xpos, ypos = cords
        lis = []

        for x in range(-1, 2):

            # if its in range
            if -1 < xpos + x < self.width:

                for y in range(-1, 2):

                    if -1 < ypos + y < self.height:

                        if abs(x) + abs(y):

                            lis.append(self.view[ypos+y][xpos+x])

        return lis

    # returns the cords of the neighbors for a position
    def cords_neighbors(self, cords):

        xpos, ypos = cords
        lis = []

        for x in range(-1, 2):

            # if its in range
            if -1 < xpos + x < self.width:

                for y in range(-1, 2):

                    if -1 < ypos + y < self.height:

                        if abs(x) + abs(y):

                            lis.append((ypos+y, xpos+x))

        return lis

    # if the player mines a square
    def mine(self, cords, recurved=False):

        xpos, ypos = cords

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
        """
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
                    self.queue.pop(-1)"""
        self.update_display()

    # flag a mine
    def flag(self, cords, event):

        xpos, ypos = cords

        if self.view[ypos][xpos] != 'F':
        
            self.view[ypos][xpos] = 'F'

        else:

            self.view[ypos][xpos] = '?'

        self.update_display()

    # add the mines
    def seed(self, xpos, ypos):

        # find all of the possible mine squares
        posminepos = [(y, x) for x in range(self.height) for y in range(self.width) if abs(x-xpos) > 0 and abs(y-ypos) > 0 and abs(x-xpos) + abs(y-ypos) > 2]

        print(posminepos)
        
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

                button = tk.Button(self.display, text=self.view[r][c], command=partial(self.mine, (c, r)))

                button.bind('<Button-3>', partial(self.flag, (c, r)))

                button.bind('<Button-2>', partial(print, self.auto_flag((c, r))))

                button.grid(row=r, column=c)

        tk.Button(self.display, text='solve', command=self.solve).grid(row=self.height+1, column=self.width+1)

    def display_mines(self):

        for f in self.mines:

            for g in f:

                print(g, end='')

            print('')

    # solve the game of mine sweeper
    def solve(self):

        working = True

        # while its still making progress
        while working:

            working = False

            # loop thru all the functions
            funcs = {self.auto_flag: 'flag', self.auto_mine: 'mine'}
            for func in funcs:

                for y in range(self.height):

                    for x in range(self.width):

                        print('new')

                        if func((x, y)):

                            working = True

                            if funcs[func] == 'mine':

                                for cords in func((x, y)):

                                    print('mining', cords)

                                    self.mine(cords)

                            else:

                                for cords in func((x, y)):

                                    print('flagging', cords)
                                    input()

                                    self.flag(cords, None)

    # return true if the game is solved. else return false.
    def solved(self):

        if sum([lis.count('?') + lis.count('F') for lis in self.view]) == self.nummines:

            return True

        else:

            return False

    # detects if the value of the square is equal the the amount of unmined neighbors
    def auto_flag(self, cords):

        xpos, ypos = cords

        # if the number of the square == the amount of neighbors
        if self.view[ypos][xpos] == self.unmined_neighbors(cords):

            # return the unflaged neighbors
            return [neighbor for neighbor in self.cords_neighbors(cords) if self.view[neighbor[1]][neighbor[0]] == '?']

    # detects if the value of the square is equal to the amount of mines
    def auto_mine(self, cords):

        xpos, ypos = cords

        # if the number of the squares == the amount of flagged neighbors
        if self.view[ypos][xpos] == self.value_neighbors(cords).count('F'):

            # mine all the squares
            return self.cords_neighbors(cords)


if __name__ == '__main__':

    s = Sweep(5, 5, 1)
    s.update_display()
    tk.mainloop()