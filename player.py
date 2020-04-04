import pygame
from settings import *

vec = pygame.math.Vector2


class Player:

    def __init__(self, app, position):
        self.app = app
        self.grid_position = position  # position is a player start position from player init
        self.pix_position = self.get_pix_position()
        self.direction = vec(1, 0)
        self.current_score = 0
        self.stored_direction = None
        self.able_to_move = True

    def get_pix_position(self):
        # player circle position on the grid map
        return vec((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def update(self):
        if self.able_to_move:
            self.pix_position += self.direction
        if self.move_next_position():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # following the player circle on grid - tracking the movement
        self.grid_position[0] = (self.pix_position[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_position[1] = (self.pix_position[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

        # check the actual grid position, and if there it has a coin, the player "eat" that
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # player circle
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_position.x), int(self.pix_position.y)),
                           self.app.cell_width // 2 - 2)
        # player position on grid for following
        # pygame.draw.rect(self.app.screen, RED,
        #                   (self.grid_position[0] * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
        #                    self.grid_position[1] * self.app.cell_height + TOP_BOTTOM_BUFFER // 2, self.app.cell_width, self.app.cell_height), 1)

    # by read keyboard movement at this moment
    def move(self, vector_dir):
        self.stored_direction = vector_dir

    # move next position check
    def move_next_position(self):
        if int(self.pix_position.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_position.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

    # check the wall, and we can move there or not
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_position + self.direction) == wall:
                return False
        return True

    def on_coin(self):
        if self.grid_position in self.app.coins and self.move_next_position():
            return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_position)
        self.current_score += 1

