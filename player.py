import pygame
from settings import *

vec = pygame.math.Vector2


class Player:

    def __init__(self, app, position):
        self.app = app
        self.grid_position = position  # position is a player start position from player init
        self.pix_position = self.get_pix_position()
        self.direction = vec(1, 0)
        self.stored_direction = None

    def get_pix_position(self):
        # player circle position on the grid map
        return vec((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def update(self):
        self.pix_position += self.direction
        if int(self.pix_position.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                if self.stored_direction is not None:
                    self.direction = self.stored_direction
        if int(self.pix_position.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                if self.stored_direction is not None:
                    self.direction = self.stored_direction

        # following the player circle on grid - tracking the movement
        self.grid_position[0] = (self.pix_position[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_position[1] = (self.pix_position[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        # player circle
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_position.x), int(self.pix_position.y)),
                           self.app.cell_width // 2 - 2)
        # player position on grid for following
        pygame.draw.rect(self.app.screen, RED,
                         (self.grid_position[0] * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
                          self.grid_position[1] * self.app.cell_height + TOP_BOTTOM_BUFFER // 2, self.app.cell_width, self.app.cell_height), 1)

    def move(self, vector_dir):
        self.stored_direction = vector_dir
