import pygame
import sys
from settings import *
from player import Player
from enemy import Enemy

pygame.init()
vec = pygame.math.Vector2


class Pac_Man:
    """
    Pac-Man Game main object, with the game parameters, and methods.
    """

    def __init__(self):
        """
        Constructor of the Pac-Man Game, with
        the game parameters.
        """
        self.running = True
        self.state = 'start'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('maze.png')
        self.cell_width = MAZE_WIDTH // COLUMNS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.enemies_pos = {}
        self.enemies = []
        self.player_pos = None

        self.load_maze_and_walls_positions()

        # first parameter -> self is a Pac-Man app class
        self.player = Player(self, vec(self.player_pos))

        self.make_enemies()

    def run(self):
        """
        Main method of the game, where the game running.
        There are 3 different state (start, playing and game over) every state has 3 method
        which are the event handler, updater and the drawing section.
        """

        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def load_maze_and_walls_positions(self):
        """
        Background picture handler, with the scaling and build the real map about the walls text file,
        where the 'B' is the game to the enemy ghosts (black rectangles to the picture)
        '1' is the parts of the wall,
        'C' the coins on the roads,
        'P' the player starting position
        numbers are the enemies (position).
        """
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # walls and coins list with coordinates of walls and coins
        # plus player position from file and enemy positions
        with open("walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x_index, y_index))
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK,
                                         (x_index * self.cell_width, y_index * self.cell_height, self.cell_width,
                                          self.cell_height))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))
                    elif char == "P":
                        self.player_pos = [x_index, y_index]
                    elif char in ["2", "3", "4", "5"]:
                        self.enemies_pos[char] = [x_index, y_index]

    def make_enemies(self):
        """
        Enemy creation, using the datas from the walls text. (enemies_pos dictionary)
        """
        for key, value in self.enemies_pos.items():
            self.enemies.append(Enemy(self, key, vec(value)))

    def remove_life(self):
        """
        Player life handler, if there is no more life the game is over otherwise the game restarting.
        """
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_position = vec(self.player.starting_position)
            self.player.pix_position = self.player.get_pix_position()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_position = vec(enemy.starting_position)
                enemy.pix_position = enemy.get_pix_position()
                enemy.direction *= 0

    def draw_grid(self):
        """
        Grid drawing to see the actual map (background) segments, situations etc.
        (not in develop status, we use only the background image).
        """
        for i in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (i * self.cell_width, 0),
                             (i * self.cell_width, HEIGHT))

        for i in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, i * self.cell_height),
                             (WIDTH, i * self.cell_height))

    def draw_walls(self):
        """
        Wall drawing to see the actual map (background) segments, situations etc.
        (not in develop status, we use only the background image).
        Check the movement and wall positions in the player class. (can_move)
        """
        for wall in self.walls:
            pygame.draw.rect(self.background, (255, 255, 255),
                             (wall.x * self.cell_width,
                              wall.y * self.cell_height, self.cell_width, self.cell_height))

    def draw_coins(self):
        """
        Coin drawing to the map. (screen)
        """
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def draw_text(self, screen, text, position, size, color, font_name, centered=False):
        """
        Custom text drawing and customization helper method.
        """
        font = pygame.font.SysFont(font_name, size)
        text_word = font.render(text, False, color)
        text_word_size = text_word.get_size()
        if centered:
            position[0] = position[0] - text_word_size[0] // 2
            position[1] = position[1] - text_word_size[1] // 2
        screen.blit(text_word, position)

    def reset(self):
        """
        Game reset to the restart in the game over event.
        """
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_position = vec(self.player.starting_position)
        self.player.pix_position = self.player.get_pix_position()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_position = vec(enemy.starting_position)
            enemy.pix_position = enemy.get_pix_position()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(x_index, y_index))
        self.state = "playing"

    def start_events(self):
        """
        Start event, to start the game with state changing or quit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        """
        Start event menu drawing with the start informations.
        """
        self.screen.fill(BLACK)
        self.draw_text(self.screen, 'PUSH SPACE TO START', [WIDTH // 2, HEIGHT // 2],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(self.screen, '1 PLAYER ONLY', [WIDTH // 2, HEIGHT // 2 + 50],
                       START_TEXT_SIZE, (33, 137, 156), START_FONT, centered=True)
        pygame.display.update()

    def playing_events(self):
        """
        Play event, with the quit option and the movement handling sections.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        """
        Playing state updating player and enemies update.
        If enemy catch the player -> remove_file and game over handling.
        """
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_position == self.player.grid_position:
                self.remove_life()

    def playing_draw(self):
        """
        Gameplay section drawing section, with the map, coins, player and enemies visualization.
        """
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        # self.draw_grid()  # draw the grid on the picture map
        # self.draw_walls()  # draw the walls on the picture map
        self.draw_coins()
        self.draw_text(self.screen, 'CURRENT SCORE: {}'.format(self.player.current_score), [60, 0],
                       18, (255, 255, 255), START_FONT, centered=False)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def game_over_events(self):
        """
        Game over event to chose, start again or quit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        """
        Game over menu drawing section, restart or quit.
        """
        self.screen.fill(BLACK)
        self.draw_text(self.screen, 'GAME OVER', [WIDTH // 2, 100],
                       36, RED, START_FONT, centered=True)
        self.draw_text(self.screen, 'SPACE TO RESTART', [WIDTH // 2, HEIGHT // 2 + 50],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(self.screen, 'ESCAPE TO QUIT', [WIDTH // 2, HEIGHT // 2 + 100],
                       START_TEXT_SIZE, (33, 137, 156), START_FONT, centered=True)
        pygame.display.update()
