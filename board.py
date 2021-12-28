from random import randint
import numpy as np
import plotly.express as px
import pandas
import plotly.graph_objects as go
from matplotlib import colors
import gif

import sys
import argparse
import os

#TODO check to see if we have seen that board config before and if so stop calculations and run in loop

class Board:
    def __init__(self, size, color1, color2):
        self._rows = size
        self._columns = size
        self.color1 = color1
        self.color2 = color2
        self.frames = []
        self.board = self.generate_board()
        self.draw_board()

    def draw_board(self):
        current_board = np.full([self._rows, self._columns, 3], self.color1)	

        for elem in self.board :
            current_board[elem[0], elem[1]] = self.color2
        fig = go.Image(z=current_board)
        self.frames.append(current_board)
        
    def generate_board(self):
        board = []
        for row in range(self._rows):
            for col in range(self._columns):
                random_number = randint(0, 7)
                if random_number == 3:
                    board.append((row, col))
        return board

    def update_board(self):
        count_neighbors = {}
        for living_cell in self.board:
            nb = self.get_neighbors(living_cell)
            if living_cell not in count_neighbors:
                count_neighbors[living_cell] = 0
            for cell in nb:
                if cell in count_neighbors:
                    count_neighbors[cell] += 1
                else:
                    count_neighbors[cell] = 1
        for cell, value in count_neighbors.items():
            self.apply_rules(cell, value)
        self.draw_board()

    def get_neighbors(self, cell):
        n = []
        if cell[0] - 1 >= 0: # over
            n.append((cell[0] - 1, cell[1]))
        if cell[0] + 1 < self._rows: #under
            n.append((cell[0] + 1, cell[1]))
        if cell[1] - 1 >= 0: #left
            n.append((cell[0], cell[1]-1))
        if cell[1] + 1 < self._columns: #right
            n.append((cell[0], cell[1] + 1))
        if (cell[0] - 1 >= 0) and (cell[1] - 1 >= 0): #upper left
            n.append((cell[0] - 1, cell[1] - 1))
        if (cell[0] - 1 >= 0) and (cell[1] + 1 < self._columns): ##upper right
            n.append((cell[0] - 1, cell[1] + 1))
        if (cell[0] + 1 < self._rows) and (cell[1] - 1 >= 0 ): #lower left
            n.append((cell[0] + 1, cell[1] - 1))
        if (cell[0] + 1 < self._rows) and (cell[1] + 1 < self._columns): #lower right
            n.append((cell[0] + 1, cell[1] + 1))
        return n

    def apply_rules(self, cell, value):
        #rules for living cells
        if cell in self.board:
            if (value < 2) or (value > 3):
                self.board.remove(cell)
        else:
            if value == 3:
                self.board.append(cell)

    def play_frames(self):
        # img_frames = [go.Frame(data=go.Image(z = x)) for x in self.frames]
        fig = go.Figure(
            data=[go.Image(z = self.frames[0])],
            layout=go.Layout(
                width=max(400, min(self._columns * 20, 1000)),
                height = max(400, min(self._rows * 20, 1000)),
                title_text="The Game of Life",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(
                            label="Play",
                            method="animate",
                            args=[None,
                                {"frame": {"duration": 100},
                                 "mode": "immediate",
                                 "fromcurrent": True, 
                                 "transition": {"duration": 100}
                                }])
                    ]
                )]
            ),
            frames=[go.Frame(data=go.Image(z=x),\
                layout = go.Layout(title_text = 'iteration {}'.format(i)))\
                    for i, x in enumerate(self.frames)]
        )
        fig.show()

    def save_frames(self):
        @gif.frame
        def plot(i):
            fig = go.Figure()
            fig.add_trace(go.Image(z = i),
            )
            fig.update_layout(                
                width=max(400, min(self._columns * 20, 1000)),
                height = max(400, min(self._rows * 20, 1000)),)
            return fig
        save_frames = []
        for x in self.frames:
            frame = plot(x)
            save_frames.append(frame)
        path = os.path.dirname(os.path.realpath(__file__))
        gif.save(save_frames, os.path.join(path, 'example.gif'), duration=100)

        



def main(args):
    size = int(input("Enter size of the simulation: [40]") or 40)
    iterations = int(input("Enter the number of iterations: [100]") or 100)
    color1 = (input("Enter the first color: [black]  ") or "black")
    color2 = (input("Enter the second color: [white]  ") or "white")
    do_save = (input("Save simulation? [True or False] ") or True)
    r1, g1, b1 = colors.to_rgb(color1)
    color1 = [r1*255,g1*255,b1*255]
    r2, g2, b2 = colors.to_rgb(color2)
    color2 = [r2*255,g2*255,b2*255]
    b = Board(int(size), color1, color2)
    for i in range(int(iterations)):
        b.update_board()
    b.play_frames()
    if do_save:
        b.save_frames()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--size')
    parser.add_argument('--iter')
    parser.add_argument('--color1')
    parser.add_argument('--color2')
    parser.add_argument('--do_save')
    args = parser.parse_args()
    main(args)
