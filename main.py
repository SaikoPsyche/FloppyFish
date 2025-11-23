import pygame
import sys
import random
from collections import deque

# -------------------------------
# Config
# -------------------------------
WIDTH, HEIGHT = 800, 800
FPS = 60

PIPE_GAP_SIZE = 150
PIPE_SPEED = 3
PIPE_FREQUENCY = 1500  # ms
GROUND_HEIGHT = 80
GRAVITY = 0.5
FLAP_STRENGTH = -9

GROUND_COLOR = (222, 184, 135)
TEXT_COLOR = (0, 0, 0)

# -------------------------------
# Sprite Loader
# -------------------------------
class SpriteLoader:
    def __init__(self):
        scale = (5, 5)
        self.background = self.load("img/background.png", scale)
        self.pipe = self.load("img/pipe.png"), 
        self.pipe_flipped = pygame.transform.flip(self.pipe, False, True)
        self.bird = self.load("img/bird.png")

    @staticmethod
    def load(path, scale=None):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img


# -------------------------------
# Bird
# -------------------------------
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


# -------------------------------
# Pipe
# -------------------------------
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


# -------------------------------
# Pipe Manager
# -------------------------------
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


# -------------------------------
# Game
# -------------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird OOP")

        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 28)

        self.sprites = SpriteLoader()
        self.reset()

    def reset(self):
        self.bird = Bird(WIDTH * 0.25, HEIGHT // 2, self.sprites.bird)
        self.pipe_manager = PipeManager(self.sprites)
        self.score = 0
        self.started = False
        self.game_over = False

    def draw_ground(self):
        pygame.draw.rect(
            self.screen,
            GROUND_COLOR,
            (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        )

    def draw_text_center(self, text, y, font):
        render = font.render(text, True, TEXT_COLOR)
        rect = render.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(render, rect)

    def check_collisions(self):
        if self.bird.y >= HEIGHT - GROUND_HEIGHT or self.bird.y <= 0:
            return True
        return self.pipe_manager.check_collisions(self.bird)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)

            # --- Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if self.bird.alive:
                            self.bird.flap()
                            self.started = True
                        elif self.game_over:
                            self.reset()

                    if event.key == pygame.K_r:
                        self.reset()

                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.bird.alive:
                        self.bird.flap()
                        self.started = True

            # --- Update ---
            if self.bird.alive and self.started:
                self.bird.update()
                self.pipe_manager.update(self.bird)
                self.score += self.pipe_manager.check_score(self.bird)

                if self.check_collisions():
                    self.bird.alive = False
                    self.game_over = True

            # --- Draw ---
            self.screen.blit(self.sprites.background, (0, 0))
            self.pipe_manager.draw(self.screen)
            self.draw_ground()
            self.bird.draw(self.screen)

            self.draw_text_center(str(self.score), 60, self.font_large)

            if not self.started:
                self.draw_text_center("Press Space / Click to Start", HEIGHT//2, self.font_small)
            if self.game_over:
                self.draw_text_center("GAME OVER", HEIGHT//2 - 60, self.font_large)
                self.draw_text_center("Press R to retry", HEIGHT//2, self.font_small)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


# -------------------------------
# Run Game
# -------------------------------
if __name__ == "__main__":
    Game().run()
