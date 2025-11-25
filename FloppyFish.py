import pygame
import random
from collections import deque
from setup import *
from pipe import Pipe


class PipeManager:
    def __init__(self, sprite_loader):
        self.pipes = deque()
        self.sprite_top = sprite_loader.pipe_flipped
        self.sprite_bottom = sprite_loader.pipe
        self.last_spawn_time = pygame.time.get_ticks() - 800

    def spawn_pipe(self):
        margin = 80
        gap_y = random.randint(
            margin + PIPE_GAP_SIZE // 2,
            HEIGHT - GROUND_HEIGHT - margin - PIPE_GAP_SIZE // 2,
        )
        pipe = Pipe(WIDTH + 50, gap_y, self.sprite_top, self.sprite_bottom)
        self.pipes.append(pipe)

    def update(self, bird):
        now = pygame.time.get_ticks()
        if bird.alive and now - self.last_spawn_time > PIPE_FREQUENCY:
            self.spawn_pipe()
            self.last_spawn_time = now

        for p in list(self.pipes):
            p.update()
            if p.off_screen():
                self.pipes.popleft()

    def draw(self, surf):
        for p in self.pipes:
            p.draw(surf)

    def check_score(self, bird):
        score = 0
        for p in self.pipes:
            if not p.passed and p.x + p.width < bird.x:
                p.passed = True
                score += 1
        return score

    def check_collisions(self, bird):
        for p in self.pipes:
            if bird.rect.colliderect(p.top_rect()) or bird.rect.colliderect(p.bottom_rect()):
                return True
        return False

