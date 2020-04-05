import pygame
from settings import *

vec = pygame.math.Vector2


class Enemy:

    def __init__(self, app, key, position):
        self.app = app
        self.key = key
        self.grid_position = position
        self.pix_position = self.get_pix_position()
        self.color = self.set_color()

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color,
                           (int(self.pix_position.x), int(self.pix_position.y)), self.app.cell_width // 2)

    def get_pix_position(self):
        # enemy position on the grid map
        return vec((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def set_color(self):
        if self.key == "2":
            return (43, 78, 203)
        if self.key == "3":
            return (197, 200, 27)
        if self.key == "4":
            return (189, 29, 29)
        if self.key == "5":
            return (215, 159, 33)
