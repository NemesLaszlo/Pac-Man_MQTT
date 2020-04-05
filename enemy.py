import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:

    def __init__(self, app, key, position):
        self.app = app
        self.key = key
        self.grid_position = position
        self.pix_position = self.get_pix_position()
        self.color = self.set_color()
        self.direction = vec(1, 0)  # when the game start not moving at all
        self.personality = self.set_personality()

    def update(self):
        self.pix_position += self.direction
        if self.move_next_position():
            self.move()

        # following the enemy circle on grid - tracking the movement
        self.grid_position[0] = (self.pix_position[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_position[1] = (self.pix_position[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

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

    def set_personality(self):
        if self.key == "2":
            return "speedy"
        if self.key == "3":
            return "slow"
        if self.key == "4":
            return "random"
        if self.key == "5":
            return "scared"

    # move next position check
    def move_next_position(self):
        if int(self.pix_position.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_position.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)


            

