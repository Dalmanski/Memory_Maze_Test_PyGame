import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 800
GRID_SIZE = 40
ROWS, COLS = 20, 10
FPS = 60
MOVE_DELAY = 500  # Delay in milliseconds before continuous movement starts
MOVE_INTERVAL = 100  # Interval in milliseconds between moves

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (192, 192, 192)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Maze Test")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Player settings
player_pos = [0, 0]  # Start at the top-left corner
player_direction = None
player_moving = False
move_start_time = None  # Time when the key was first pressed
last_move_time = None  # Time when the last move occurred

# Game state
red_tiles = []
game_started = False
game_over = False
game_won = False  # New flag to track if the player has won

# Finish line
finish_line = (ROWS - 1, COLS - 1)  # Bottom-right corner

# Generate random red tiles
def generate_red_tiles():
    global red_tiles
    red_tiles = []
    for _ in range(20):  # Adjust the number of red tiles as needed
        while True:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if (row, col) not in red_tiles and (row, col) != finish_line and (row, col) != (0, 0):
                red_tiles.append((row, col))
                break

generate_red_tiles()

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid outline


def draw_tiles():
    for tile in red_tiles:
        row, col = tile
        rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        if game_over:
            pygame.draw.rect(screen, RED, rect)  # Always show red tiles during game over
        elif not game_started:
            pygame.draw.rect(screen, RED, rect)  # Show red tiles before start
        else:
            # Create a surface with per-pixel alpha for transparency
            tile_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            tile_surface.fill((255, 0, 0, 0))  # Fill with red and 0 alpha (completely transparent)
            screen.blit(tile_surface, rect.topleft)  # Blit the transparent tile onto the screen


def draw_player():
    row, col = player_pos
    rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, BLUE, rect)


def draw_finish_line():
    row, col = finish_line
    rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, GREEN, rect)


def show_game_over():
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


def show_you_win():
    text = font.render("You Win!", True, GREEN)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


def show_start_button():
    text = font.render("Start", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, GREY, button_rect)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    return button_rect


def show_try_again_button():
    text = font.render("Try Again", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 120, 50)
    pygame.draw.rect(screen, GREY, button_rect)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50 + 10))
    return button_rect


def move_player():
    global game_over, game_won
    if player_direction == "UP":
        if player_pos[0] > 0:
            player_pos[0] -= 1
    elif player_direction == "DOWN":
        if player_pos[0] < ROWS - 1:
            player_pos[0] += 1
    elif player_direction == "LEFT":
        if player_pos[1] > 0:
            player_pos[1] -= 1
    elif player_direction == "RIGHT":
        if player_pos[1] < COLS - 1:
            player_pos[1] += 1

    # Check for collision with red tiles
    if tuple(player_pos) in red_tiles:
        game_over = True

    # Check for reaching the finish line
    if tuple(player_pos) == finish_line:
        game_won = True


def reset_game():
    global player_pos, player_direction, player_moving, game_started, game_over, game_won
    player_pos = [0, 0]
    player_direction = None
    player_moving = False
    game_started = False
    game_over = False
    game_won = False
    generate_red_tiles()

# Main loop
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_tiles()
    draw_player()
    draw_finish_line()

    if not game_started and not game_over and not game_won:
        start_button = show_start_button()

    if game_over:
        show_game_over()
        try_again_button = show_try_again_button()

    if game_won:
        show_you_win()
        try_again_button = show_try_again_button()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_direction != "UP":
            player_direction = "UP"
            player_moving = True
            move_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - move_start_time >= MOVE_DELAY:
                if last_move_time is None or pygame.time.get_ticks() - last_move_time >= MOVE_INTERVAL:
                    player_moving = True
                    last_move_time = pygame.time.get_ticks()

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_direction != "DOWN":
            player_direction = "DOWN"
            player_moving = True
            move_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - move_start_time >= MOVE_DELAY:
                if last_move_time is None or pygame.time.get_ticks() - last_move_time >= MOVE_INTERVAL:
                    player_moving = True
                    last_move_time = pygame.time.get_ticks()

    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_direction != "LEFT":
            player_direction = "LEFT"
            player_moving = True
            move_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - move_start_time >= MOVE_DELAY:
                if last_move_time is None or pygame.time.get_ticks() - last_move_time >= MOVE_INTERVAL:
                    player_moving = True
                    last_move_time = pygame.time.get_ticks()

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_direction != "RIGHT":
            player_direction = "RIGHT"
            player_moving = True
            move_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - move_start_time >= MOVE_DELAY:
                if last_move_time is None or pygame.time.get_ticks() - last_move_time >= MOVE_INTERVAL:
                    player_moving = True
                    last_move_time = pygame.time.get_ticks()

    else:
        player_direction = None
        player_moving = False
        move_start_time = None
        last_move_time = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and not game_over and not game_won and start_button.collidepoint(event.pos):
                game_started = True
                player_moving = True
            elif (game_over or game_won) and try_again_button.collidepoint(event.pos):
                reset_game()

    if player_moving and game_started and not game_over and not game_won:
        move_player()
        player_moving = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
