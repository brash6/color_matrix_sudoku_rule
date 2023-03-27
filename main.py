import numpy as np
import random
import panel as pn
import param
import math
from random import randint

from bokeh.palettes import Category20_20, Spectral10
from sudoku_generator import makeBoard

palette = Spectral10
nb_add_colors = 0


class MatrixColorChoice(param.Parameterized):
    number_of_color = param.Integer(9)
    refresh_matrix = param.Action(label="REFRESH MATRIX", doc="Refreshes the matrix")
    view = param.Parameter()

    def __init__(self, **params):
        super().__init__(**params)
        self.number_of_color = 9

        self.refresh_matrix_button = pn.Param(
            self,
            name="",
            parameters=["refresh_matrix"],
            widgets={"refresh_matrix": pn.widgets.Button(name="Refresh Matrix"),
                     }
        )

        board = makeBoard()
        self.matrix = np.array(board) - 1
        self.color_list = list(palette[: self.number_of_color + nb_add_colors])
        self.list_color_matrix = []
        self.build_color_list_from_sudoku()

        self.matrix_panel = pn.GridBox(*[pn.pane.HTML(
            background=self.list_color_matrix[i],
            width=50,
            height=50
        ) for i in range(self.number_of_color * self.number_of_color)],
                                       ncols=self.number_of_color)

        self.view = pn.Column(self.refresh_matrix_button, self.matrix_panel)

        self.refresh_matrix = self._build_sudoku_matrix

    def _build_sudoku_matrix(self, event):
        board = makeBoard()
        self.matrix = np.array(board) - 1
        self.color_list = list(palette[: self.number_of_color + nb_add_colors])
        self.list_color_matrix = []
        self.build_color_list_from_sudoku()

        self.matrix_panel = pn.GridBox(*[pn.pane.HTML(
            background=self.list_color_matrix[i],
            width=50,
            height=50
        ) for i in range(self.number_of_color * self.number_of_color)],
                                       ncols=self.number_of_color)

        self.view[1] = self.matrix_panel

        return True

    def build_color_list_from_sudoku(self):
        for i in range(CONST_SIZE):
            for j in range(CONST_SIZE):
                self.list_color_matrix.append(self.color_list[int(self.matrix[i][j])])

    def _re_build_matrix(self, event):
        board = makeBoard()
        self.matrix = np.array(board) - 1
        self.color_list = list(palette[: self.number_of_color + nb_add_colors])
        self.list_color_matrix = []
        self.build_matrix()

        self.matrix_panel = pn.GridBox(*[pn.pane.HTML(
            background=self.list_color_matrix[i],
            width=50,
            height=50
        ) for i in range(self.number_of_color * self.number_of_color)],
                                       ncols=self.number_of_color)

        self.view[1] = self.matrix_panel

        return True

    def build_matrix(self):
        for i in np.arange(self.number_of_color):
            line_already_used_colors = []
            for j in np.arange(self.number_of_color):
                if i == j == 0:
                    self.init_first_color()
                    line_already_used_colors.append(int(self.matrix[i][j]))
                else:
                    column_already_use_color = []
                    for k in range(i):
                        column_already_use_color.append(int(self.matrix[k][j]))

                    possible_colors = self.get_possible_colors(i, j, line_already_used_colors, column_already_use_color)
                    print(possible_colors)
                    if not possible_colors:
                        self.matrix = np.full([self.number_of_color, self.number_of_color], np.nan)
                        self.color_list = list(palette[: self.number_of_color + nb_add_colors])
                        self.list_color_matrix = []
                        self.build_matrix()
                    else:
                        self.matrix[i][j] = random.choice(list(possible_colors))
                        line_already_used_colors.append(int(self.matrix[i][j]))

                self.list_color_matrix.append(self.color_list[int(self.matrix[i][j])])

    def init_first_color(self):
        rand_color_index = randint(low=0, high=self.number_of_color + nb_add_colors, size=1)[0]
        self.matrix[0][0] = int(rand_color_index)

    def get_possible_colors(self, i, j, line_already_used_colors, column_already_use_color):
        if i == 0 and j > 0:
            elems = [int(self.matrix[i][j - 1])]
        elif j == 0 and i > 0:
            elems = [int(self.matrix[i - 1][j])]
        else:
            elems = [int(self.matrix[i - 1][j]), int(self.matrix[i][j - 1])]

        possible_colors = list(np.arange(self.number_of_color + nb_add_colors))
        possible_colors_final = [item for item in possible_colors if item not in elems]
        possible_colors_unique = [item for item in possible_colors_final if item not in line_already_used_colors]
        possible_colors_unique_final = [item for item in possible_colors_unique if item not in column_already_use_color]

        return possible_colors_unique_final


MatrixColorChoice().view.servable()
