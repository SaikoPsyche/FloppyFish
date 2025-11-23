import pygame
from setup import *

class Pipe:
    def __init__(self, x, gap_y, sprite_top, sprite_bottom):
        self.x = x
        self.gap_y = gap_y
        self.sprite_top = sprite_top
        self.sprite_bottom = sprite_bottom
        self.width = sprite_top.get_width()
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x + self.width < 0

    def top_rect(self):
        return self.sprite_top.get_rect(
            midbottom=(self.x + self.width // 2, self.gap_y - PIPE_GAP_SIZE // 2)
        )

    def bottom_rect(self):
        return self.sprite_bottom.get_rect(
            midtop=(self.x + self.width // 2, self.gap_y + PIPE_GAP_SIZE // 2)
        )

    def draw(self, surf):
        surf.blit(self.sprite_top, self.top_rect())
        surf.blit(self.sprite_bottom, self.bottom_rect())