import pygame
from setup import *

class Pipe:
    def __init__(self, pipe_img, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.passed = False
        self.width = pipe_img.get_width()
        self.height = pipe_img.get_height()
        self.top_img = pygame.transform.flip(pipe_img, False, True)
        self.bottom_img = pipe_img

    def update(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x + self.width < 0

    def draw(self, surf):
        top_rect = self.top_img.get_rect(midbottom=(self.x + self.width // 2, self.gap_y - PIPE_GAP_SIZE // 2))
        bottom_rect = self.bottom_img.get_rect(midtop=(self.x + self.width // 2, self.gap_y + PIPE_GAP_SIZE // 2))
        surf.blit(self.top_img, top_rect)
        surf.blit(self.bottom_img, bottom_rect)

    def top_rect(self):
        return self.top_img.get_rect(midbottom=(self.x + self.width // 2, self.gap_y - PIPE_GAP_SIZE // 2))

    def bottom_rect(self):
        return self.bottom_img.get_rect(midtop=(self.x + self.width // 2, self.gap_y + PIPE_GAP_SIZE // 2))