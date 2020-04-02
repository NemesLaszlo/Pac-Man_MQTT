import pygame
import sys
from settings import *

pygame.init()
vec = pygame.math.Vector2


class Pac_Man:

    def __init__(self):
        self.running = True
        self.state = 'start'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

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
        self.screen.fill(RED)
        pygame.display.update()




