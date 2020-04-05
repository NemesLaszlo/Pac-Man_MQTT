import pygame
from settings import *

vec = pygame.math.Vector2


class Enemy:

    def __init__(self, app, position):
        self.app = app
        self.grid_position = position
        self.pix_position = self.get_pix_position()

    def get_pix_position(self):
        # enemy position on the grid map
        return vec((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen, (255, 255, 255),
                           (int(self.pix_position.x), int(self.pix_position.y)), self.app.cell_width // 2 - 2)

