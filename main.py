import pygame
import sys
from setup import *
from fish import Bird
from floppyFish import PipeManager


class SpriteLoader:
    def __init__(self):
        self.background = self.load("img/background.png", (WIDTH, HEIGHT))
        self.pipe = self.load("img/pipe.png")
        self.pipe_flipped = pygame.transform.flip(self.pipe, False, True)
        self.bird = self.load("img/bird.png")

    @staticmethod
    def load(path, scale=None):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Floppy Fish")

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
