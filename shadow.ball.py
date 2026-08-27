import pygame
import random
import math

pygame.init()

# =========================
# SETTINGS
# =========================

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHADOW ESCAPE")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================

BLACK = (10, 10, 18)
BLUE = (50, 150, 255)
RED = (255, 60, 80)
YELLOW = (255, 220, 50)
WHITE = (240, 240, 240)
PURPLE = (150, 80, 255)
GREEN = (50, 255, 150)

# =========================
# PLAYER
# =========================

player_size = 30

player = pygame.Rect(
    WIDTH // 2,
    HEIGHT // 2,
    player_size,
    player_size
)

player_speed = 5

# =========================
# SHADOW
# =========================

shadow_size = 35

shadow = pygame.Rect(
    100,
    100,
    shadow_size,
    shadow_size
)

shadow_speed = 2.0

# =========================
# ORB
# =========================

orb_size = 15

orb = pygame.Rect(
    random.randint(50, WIDTH - 50),
    random.randint(50, HEIGHT - 50),
    orb_size,
    orb_size
)

# =========================
# GAME VARIABLES
# =========================

score = 0
high_score = 0

game_over = False

font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 80)


# =========================
# NEW ORB
# =========================

def create_orb():

    x = random.randint(40, WIDTH - 40)
    y = random.randint(40, HEIGHT - 40)

    return pygame.Rect(
        x,
        y,
        orb_size,
        orb_size
    )


# =========================
# RESET GAME
# =========================

def reset_game():

    global score
    global shadow_speed
    global game_over

    player.x = WIDTH // 2
    player.y = HEIGHT // 2

    shadow.x = 100
    shadow.y = 100

    score = 0

    shadow_speed = 2.0

    game_over = False


# =========================
# MAIN GAME LOOP
# =========================

running = True

while running:

    # =====================
    # EVENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:

                if game_over:
                    reset_game()

    # =====================
    # GAME LOGIC
    # =====================

    if not game_over:

        keys = pygame.key.get_pressed()

        # Player movement

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= player_speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += player_speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= player_speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += player_speed

        # Keep player inside screen

        if player.left < 0:
            player.left = 0

        if player.right > WIDTH:
            player.right = WIDTH

        if player.top < 0:
            player.top = 0

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT

        # =====================
        # SHADOW AI
        # =====================

        dx = player.centerx - shadow.centerx
        dy = player.centery - shadow.centery

        distance = math.sqrt(dx * dx + dy * dy)

        if distance != 0:

            dx /= distance
            dy /= distance

            shadow.x += dx * shadow_speed
            shadow.y += dy * shadow_speed

        # =====================
        # ORB COLLECTION
        # =====================

        if player.colliderect(orb):

            score += 1

            orb = create_orb()

            # Increase difficulty

            if score % 10 == 0:
                shadow_speed = shadow_speed * math.exp(.5)

        # =====================
        # SHADOW COLLISION
        # =====================

        if player.colliderect(shadow):

            game_over = True

            if score > high_score:
                high_score = score

    # =========================
    # DRAW BACKGROUND
    # =========================

    screen.fill(BLACK)

    # =========================
    # GRID
    # =========================

    for x in range(0, WIDTH, 50):

        pygame.draw.line(
            screen,
            (25, 25, 40),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, 50):

        pygame.draw.line(
            screen,
            (25, 25, 40),
            (0, y),
            (WIDTH, y)
        )

    # =========================
    # DRAW ORB
    # =========================

    pygame.draw.circle(
        screen,
        YELLOW,
        orb.center,
        orb_size
    )

    # Glow effect

    pygame.draw.circle(
        screen,
        (100, 80, 20),
        orb.center,
        orb_size + 8,
        2
    )

    # =========================
    # DRAW PLAYER
    # =========================

    pygame.draw.rect(
        screen,
        BLUE,
        player,
        border_radius=8
    )

    # Player eye

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 20, player.y + 8),
        5
    )

    # =========================
    # DRAW SHADOW
    # =========================

    pygame.draw.circle(
        screen,
        RED,
        shadow.center,
        shadow_size // 2
    )

    # Shadow eyes

    pygame.draw.circle(
        screen,
        WHITE,
        (shadow.x + 10, shadow.y + 12),
        4
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (shadow.x + 25, shadow.y + 12),
        4
    )

    # =========================
    # SCORE
    # =========================

    score_text = font.render(
        f"Energy: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    # =========================
    # HIGH SCORE
    # =========================

    high_text = font.render(
        f"Best: {high_score}",
        True,
        GREEN
    )

    screen.blit(
        high_text,
        (20, 60)
    )

    # =========================
    # DIFFICULTY
    # =========================

    speed_text = font.render(
        f"Shadow Speed: {shadow_speed:.1f}",
        True,
        PURPLE
    )

    screen.blit(
        speed_text,
        (WIDTH - 250, 20)
    )

    # =========================
    # GAME OVER
    # =========================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        game_over_text = big_font.render(
            "THE SHADOW GOT YOU!",
            True,
            RED
        )

        score_text = font.render(
            f"Energy Collected: {score}",
            True,
            WHITE
        )

        restart_text = font.render(
            "Press SPACE to escape again",
            True,
            YELLOW
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 -
                game_over_text.get_width() // 2,
                200
            )
        )

        screen.blit(
            score_text,
            (
                WIDTH // 2 -
                score_text.get_width() // 2,
                300
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                360
            )
        )

    # =========================
    # UPDATE SCREEN
    # =========================

    pygame.display.flip()

    clock.tick(60)


pygame.quit()