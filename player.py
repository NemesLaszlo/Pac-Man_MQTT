import pygame

from settings import *

vec = pygame.math.Vector2


class Player:

    def __init__(self, app, position):
        self.app = app
        self.grid_position = position
        self.pix_position = \
            vec((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_BUFFER / 2 + self.app.cell_width // 2,
            (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_BUFFER / 2 + self.app.cell_height // 2)
        print(self.grid_position, self.pix_position)

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_position.x), int(self.pix_position.y)),
                           self.app.cell_width // 2 - 2)
