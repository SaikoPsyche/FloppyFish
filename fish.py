import pygame
from setup import *

class Bird:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.vel = 0
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center=(self.x, self.y))
        self.alive = True

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.centery = self.y

    def draw(self, surf):
        rotated = pygame.transform.rotate(self.sprite, -self.vel * 3)
        rect = rotated.get_rect(center=(self.x, self.y))
        surf.blit(rotated, rect)