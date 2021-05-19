import pygame as pg 
import numpy as np

class Settings:
    """A class to store all settings for Sudoku"""

    def __init__(self):
        """Initialize the game's settings"""
        #Screen Settings
        self.screen_multiplier = 10
        self.screen_size = 90
        self.screen_width = self.screen_size * self.screen_multiplier + 300
        self.screen_height = self.screen_size * self.screen_multiplier
        self.bg_color = (200, 200, 200)

        #box settings
        self.square_size = self.screen_size * self.screen_multiplier // 3
        self.cell_size = self.square_size // 3

        #mouse coordinates
        self.mouse_x = self.screen_width + 100
        self.mouse_y = self.screen_height + 100

        #box/grid settings
        self.grid = [[str() for x in range(0,9)] for y in range(0,9)]
        self.current_x_coord = 0
        self.current_y_coord = 0
        self.selected_box_x = self.current_x_coord // 100
        self.selected_box_y = self.current_y_coord // 100

        #win conditions
        self.isFull = False
        self.hasError = False
        self.win = False

        #Number inputted
        self.input = ''

        #Clock
        self.clock = pg.time.Clock()
        self.frame_count = 0
        self.frame_rate = 60

        #Font
        pg.font.init()
        self.font = pg.font.SysFont('Arial', 100)
        self.clockFont = pg.font.SysFont('Arial', 50)
