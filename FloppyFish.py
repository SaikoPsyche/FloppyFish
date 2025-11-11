import pygame
import sys
import random
from collections import deque
from setup import *
from fish import Bird
from pipe import Pipe

class GameLoop:
    # --- Init ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Sprite Clone")
    clock = pygame.time.Clock()

    font_large = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 28)

    # --- Load Images ---
    def load_image(name, scale=None, flip=False):
        img = pygame.image.load(name).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        if flip:
            img = pygame.transform.flip(img, False, True)
        return img

    try:
        background_img = load_image("./img/background.png", (WIDTH, HEIGHT))
        bird_img = load_image("./img/bird.png")
        pipe_img = load_image("./img/pipe.png")
    except Exception as e:
        print("Error loading images:", e)
        print("Make sure background.png, bird.png, and pipe.png are in this folder.")
        sys.exit()

    # scale ground color overlay for bottom
    ground_color = (222, 184, 135)

    # --- Functions ---
    def reset_game(self):
        bird = Bird(self.bird_img, WIDTH * 0.25, HEIGHT // 2)
        pipes = Pipe(self.pipe_img, )
        score = 0
        last_pipe_time = pygame.time.get_ticks() - 800
        started = False
        return bird, pipes, score, last_pipe_time, started

    def spawn_pipe(self):
        margin = 80
        gap_y = random.randint(margin + PIPE_GAP_SIZE // 2, HEIGHT - GROUND_HEIGHT - margin - PIPE_GAP_SIZE // 2)
        return self.Pipe(WIDTH + 50, gap_y)

    def draw_ground(self):
        pygame.draw.rect(self.screen, self.ground_color, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    def check_collisions(self, bird, pipes):
        bird_rect = bird.rect
        if bird.y >= HEIGHT - GROUND_HEIGHT or bird.y <= 0:
            return True
        for p in pipes:
            if bird_rect.colliderect(p.top_rect()) or bird_rect.colliderect(p.bottom_rect()):
                return True
        return False

    def draw_text_center(surf, text, y, font, color=(0, 0, 0)):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(WIDTH // 2, y))
        surf.blit(rendered, rect)

    # --- Main Loop ---

    def run(self):
        bird, pipes, score, last_pipe_time, started = self.reset_game()
        running = True
        game_over = False

        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if bird.alive:
                            bird.flap()
                            started = True
                        elif game_over:
                            bird, pipes, score, last_pipe_time, started = self.reset_game()
                            game_over = False
                    elif event.key == pygame.K_r:
                        bird, pipes, score, last_pipe_time, started = self.reset_game()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if bird.alive:
                        bird.flap()
                        started = True

            # Spawn pipes
            now = pygame.time.get_ticks()
            if started and bird.alive and now - last_pipe_time > PIPE_FREQUENCY:
                pipes.append(self.spawn_pipe())
                last_pipe_time = now

            # Update
            if bird.alive and started:
                bird.update()
                for p in list(pipes):
                    p.update()
                    if not p.passed and p.x + p.width < bird.x:
                        p.passed = True
                        score += 1
                    if p.off_screen():
                        pipes.popleft()

                if self.check_collisions(bird, pipes):
                    bird.alive = False
                    game_over = True

            # Draw
            self.screen.blit(self.background_img, (0, 0))
            for p in pipes:
                p.draw(self.screen)
            self.draw_ground()
            bird.draw(self.screen)
            self.draw_text_center(self.screen, str(score), 60, self.font_large)

            if not started:
                self.draw_text_center(self.screen, "Press Space / Click to Start", HEIGHT // 2 - 30, self.font_small)
            if game_over:
                self.draw_text_center(self.screen, "GAME OVER", HEIGHT // 2 - 70, self.font_large)
                self.draw_text_center(self.screen, f"Score: {score}", HEIGHT // 2 - 20, self.font_small)
                self.draw_text_center(self.screen, "Press R to play again", HEIGHT // 2 + 20, self.font_small)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
