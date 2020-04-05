import pygame
import sys
from settings import *
from player import Player
from enemy import Enemy

pygame.init()
vec = pygame.math.Vector2


class Pac_Man:

    def __init__(self):
        self.running = True
        self.state = 'start'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('maze.png')
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.walls = []
        self.coins = []
        self.enemies_pos = {}
        self.enemies = []
        self.player_pos = None

        self.load_maze_and_walls_positions()

        # first parameter -> self is a Pac-Man app class
        self.player = Player(self, self.player_pos)

        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def load_maze_and_walls_positions(self):
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
                                         (x_index * self.cell_width, y_index * self.cell_height, self.cell_width, self.cell_height))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))
                    elif char == "P":
                        self.player_pos = vec(x_index, y_index)
                    elif char in ["2", "3", "4", "5"]:
                        self.enemies_pos[char] = vec(x_index, y_index)

    def make_enemies(self):
        for key, value in self.enemies_pos.items():
            self.enemies.append(Enemy(self, key, value))


    def draw_grid(self):
        for i in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (i * self.cell_width, 0),
                             (i * self.cell_width, HEIGHT))

        for i in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, i * self.cell_height),
                             (WIDTH, i * self.cell_height))

    def draw_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.background, (255, 255, 255),
                             (wall.x * self.cell_width,
                              wall.y * self.cell_height, self.cell_width, self.cell_height))

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def draw_text(self, screen, text, position, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text_word = font.render(text, False, color)
        text_word_size = text_word.get_size()
        if centered:
            position[0] = position[0] - text_word_size[0] // 2
            position[1] = position[1] - text_word_size[1] // 2
        screen.blit(text_word, position)

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, 'PUSH SPACE TO START', [WIDTH // 2, HEIGHT // 2],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(self.screen, '1 PLAYER ONLY', [WIDTH // 2, HEIGHT // 2 + 50],
                       START_TEXT_SIZE, (33, 137, 156), START_FONT, centered=True)
        self.draw_text(self.screen, 'HIGH SCORE', [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

    def playing_events(self):
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
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        # self.draw_grid()  # draw the grid on the picture map
        # self.draw_walls()  # draw the walls on the picture map
        self.draw_coins()
        self.draw_text(self.screen, 'CURRENT SCORE: {}'.format(self.player.current_score), [60, 0],
                       18, (255, 255, 255), START_FONT, centered=False)
        self.draw_text(self.screen, 'HIGH SCORE: 0', [WIDTH // 2 + 60, 0],
                       18, (255, 255, 255), START_FONT, centered=False)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
