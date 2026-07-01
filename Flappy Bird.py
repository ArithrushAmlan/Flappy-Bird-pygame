import pygame
import random
import sys


pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# Colors
BG = (135, 206, 235)      # sky
BIRD_C = (255, 220, 0)    # yellow
PIPE_C = (0, 180, 0)      # green
GROUND_C = (200, 170, 120)
TEXT_C = (20, 20, 20)

# ------------------ Game constants ------------------
GRAVITY = 0.45
JUMP_VEL = -8.5

PIPE_W = 90
PIPE_GAP = 170
PIPE_SPEED = 3.5
PIPE_SPAWN_MS = 1300

GROUND_H = 80

# ------------------ Game objects ------------------
bird = pygame.Rect(120, HEIGHT // 2 - 20, 40, 30)
bird_vel = 0

pipes = []  # each item: [top_rect, bottom_rect, scored_bool]
last_pipe_time = 0

score = 0
game_over = False
game_started = False

def make_pipe():
    gap_y = random.randint(140, HEIGHT - GROUND_H - 140)
    top_h = gap_y - PIPE_GAP // 2
    bottom_y = gap_y + PIPE_GAP // 2
    bottom_h = (HEIGHT - GROUND_H) - bottom_y

    x = WIDTH + 10
    top = pygame.Rect(x, 0, PIPE_W, top_h)
    bottom = pygame.Rect(x, bottom_y, PIPE_W, bottom_h)
    return [top, bottom, False]

def reset():
    global bird, bird_vel, pipes, last_pipe_time, score, game_over, game_started
    bird = pygame.Rect(120, HEIGHT // 2 - 20, 40, 30)
    bird_vel = 0
    pipes = []
    last_pipe_time = pygame.time.get_ticks()
    score = 0
    game_over = False
    game_started = False

reset()

# ------------------ Main loop ------------------
running = True
while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump (Space / Up)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if not game_started:
                    game_started = True
                    bird_vel = JUMP_VEL
                elif not game_over:
                    bird_vel = JUMP_VEL
                else:
                    reset()

            if event.key == pygame.K_r:
                reset()

        # Jump (Mouse Click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                game_started = True
                bird_vel = JUMP_VEL
            elif not game_over:
                bird_vel = JUMP_VEL
            else:
                reset()

    # --- Game Logic (Only runs when game is active) ---
    if game_started and not game_over:
        if now - last_pipe_time >= PIPE_SPAWN_MS:
            pipes.append(make_pipe())
            last_pipe_time = now

        # Birds
        bird_vel += GRAVITY
        bird.y += int(bird_vel)

        # Move pipes
        for p in pipes:
            p[0].x -= int(PIPE_SPEED)
            p[1].x -= int(PIPE_SPEED)

        # Remove off-screen pipes
        pipes = [p for p in pipes if p[0].right > -10]

        # Collisions & scoring
        if bird.top < 0:
            bird.top = 0
            bird_vel = 0
        if bird.bottom >= HEIGHT - GROUND_H:
            bird.bottom = HEIGHT - GROUND_H
            game_over = True

        for p in pipes:
            top, bottom, scored = p
            if bird.colliderect(top) or bird.colliderect(bottom):
                game_over = True

            # Score when bird passes pipe
            if not scored and top.right < bird.left:
                p[2] = True
                score += 1

    # ------------------ Draw Screen ------------------
    screen.fill(BG)

    # Pipes
    for p in pipes:
        pygame.draw.rect(screen, PIPE_C, p[0])
        pygame.draw.rect(screen, PIPE_C, p[1])

    # Ground
    pygame.draw.rect(screen, GROUND_C, (0, HEIGHT - GROUND_H, WIDTH, GROUND_H))

    # Bird
    pygame.draw.rect(screen, BIRD_C, bird)

    # Score text
    score_surf = font.render(str(score), True, TEXT_C)
    screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))
    

    if not game_started:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font.render("FLAPPY BIRD", True, (255, 255, 255))
        msg = small_font.render("Press SPACE or Click to Start", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))


    if game_over:
        msg1 = font.render("GAME OVER", True, (200, 40, 40))
        msg2 = small_font.render("Press SPACE / Click to Restart", True, TEXT_C)
        screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()