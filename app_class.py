import pygame
import sys
from settings import *
from player import Player

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
        self.player = Player(self, PLAYER_START_POSITION)

        self.load_maze()

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

    def load_maze(self):
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

    def draw_grid(self):
        for i in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (i * self.cell_width, 0),
                             (i * self.cell_width, HEIGHT))

        for i in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, i*self.cell_height),
                             (WIDTH, i*self.cell_height))

    def draw_text(self, screen, text, position, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text_word = font.render(text, False, color)
        text_word_size = text_word.get_size()
        if centered:
            position[0] = position[0] - text_word_size[0] / 2
            position[1] = position[1] - text_word_size[1] / 2
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
        self.draw_text(self.screen, 'PUSH SPACE TO START', [WIDTH/2, HEIGHT/2],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(self.screen, '1 PLAYER ONLY', [WIDTH / 2, HEIGHT / 2 + 50],
                       START_TEXT_SIZE, (33, 137, 156), START_FONT, centered=True)
        self.draw_text(self.screen, 'HIGH SCORE', [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        pass

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER / 2, TOP_BOTTOM_BUFFER / 2))
        self.draw_grid()
        self.draw_text(self.screen, 'CURRENT SCORE: 0', [60, 0],
                       18, (255, 255, 255), START_FONT, centered=False)
        self.draw_text(self.screen, 'HIGH SCORE: 0', [WIDTH / 2 + 60, 0],
                       18, (255, 255, 255), START_FONT, centered=False)
        self.player.draw()
        pygame.display.update()






