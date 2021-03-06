import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    """
    Player class with the methods and parameters.
    """

    def __init__(self, app, position):
        """
        Constructor of the Player, with
        the parameters.
        """
        self.app = app
        self.grid_position = position  # position is a player start position from player init
        self.pix_position = self.get_pix_position()
        self.starting_position = [position.x, position.y]
        self.direction = vec(1, 0)
        self.speed = 2
        self.current_score = 0
        self.stored_direction = None
        self.able_to_move = True
        self.lives = 1

    def update(self):
        """
        Player move check and update to work correctly.
        """
        if self.able_to_move:
            self.pix_position += self.direction * self.speed
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
        """
        Drawing the player circle and the the informations about the player lives count.
        """

        # player circle
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_position.x), int(self.pix_position.y)),
                           self.app.cell_width // 2 - 2)

        # drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (30 + 20 * x, HEIGHT - 15), 7)

        # player position on grid for following
        # pygame.draw.rect(self.app.screen, RED,
        #                   (self.grid_position[0] * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
        #                    self.grid_position[1] * self.app.cell_height + TOP_BOTTOM_BUFFER // 2, self.app.cell_width, self.app.cell_height), 1)

    def get_pix_position(self):
        # player circle position on the grid map
        return vec((self.grid_position[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_position[1] * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    # by read keyboard movement at this moment
    def move(self, vector_dir):
        """
        By read keyboard movement at this moment. "Special moving with direction storing and moving"
        """
        self.stored_direction = vector_dir

    # move next position check
    def move_next_position(self):
        """
        Moving to the next position checker.
        """
        if int(self.pix_position.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_position.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # check the wall, and we can move there or not
    def can_move(self):
        """
        Check the wall, can we move there or not.
        """
        for wall in self.app.walls:
            if vec(self.grid_position + self.direction) == wall:
                return False
        return True

    def on_coin(self):
        """
        Check the player position on a grid, is there a coin or there is no coin there.
        """
        if self.grid_position in self.app.coins and self.move_next_position():
            return True
        return False

    def eat_coin(self):
        """
        Coin "eating" and score increase.
        """
        self.app.coins.remove(self.grid_position)
        self.current_score += 1

