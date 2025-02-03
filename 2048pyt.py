import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 450  # Adjusted to make space for the score display and game over screen
TILE_SIZE = 100
GRID_SIZE = 4
FONT = pygame.font.Font(None, 50)
BUTTON_FONT = pygame.font.Font(None, 36)

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Initialize game variables
score = 0
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Helper functions
def get_empty_positions():
    empty = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                empty.append((i, j))
    return empty

def add_random_tile():
    empty = get_empty_positions()
    if not empty:
        return False
    i, j = random.choice(empty)
    grid[i][j] = 2 if random.random() < 0.9 else 4
    return True

def merge_row(row):
    # Remove all zeros and move non-zero tiles to the left
    non_empty = [x for x in row if x != 0]
    merged = []
    skip = False
    for i in range(len(non_empty)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_empty) and non_empty[i] == non_empty[i + 1]:
            merged.append(non_empty[i] * 2)
            global score
            score += merged[-1]
            skip = True
        else:
            merged.append(non_empty[i])
    return merged + [0] * (GRID_SIZE - len(merged))

def rotate_grid():
    return [list(row) for row in zip(*grid[::-1])]

def move(direction):
    global grid
    moved = False
    if direction in ['left', 'right']:
        for i in range(GRID_SIZE):
            original_row = grid[i]
            new_row = merge_row(original_row if direction == 'left' else original_row[::-1])
            if direction == 'right':
                new_row = new_row[::-1]
            if new_row != original_row:
                grid[i] = new_row
                moved = True
    else:  # 'up' or 'down'
        for j in range(GRID_SIZE):
            column = [grid[i][j] for i in range(GRID_SIZE)]
            merged_column = merge_row(column if direction == 'up' else column[::-1])
            if direction == 'down':
                merged_column = merged_column[::-1]
            for i in range(GRID_SIZE):
                if grid[i][j] != merged_column[i]:
                    grid[i][j] = merged_column[i]
                    moved = True
    return moved

def check_game_over():
    if get_empty_positions():
        return False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i + 1 < GRID_SIZE and grid[i][j] == grid[i + 1][j]:
                return False
            if j + 1 < GRID_SIZE and grid[i][j] == grid[i][j + 1]:
                return False
    return True

def draw_board(screen):
    screen.fill(BACKGROUND_COLOR)
    # Draw the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            color = TILE_COLORS.get(value, EMPTY_TILE_COLOR)
            pygame.draw.rect(screen, color, (j * TILE_SIZE, i * TILE_SIZE + 50, TILE_SIZE, TILE_SIZE))  # Offset grid to avoid overlap with score
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2 + 50))
                screen.blit(text, text_rect)
    
    # Draw the score at the top
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))  # Centered at the top

    pygame.display.flip()

def show_game_over(screen):
    game_over_text = FONT.render("Game Over", True, (0, 0, 0))
    final_score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    
    # Draw Game Over Text
    screen.fill((255, 255, 255))  # Fill screen with white
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    
    # Draw Try Again Button
    try_again_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 50)
    pygame.draw.rect(screen, (50, 150, 50), try_again_button)
    try_again_text = BUTTON_FONT.render("Try Again", True, (255, 255, 255))
    screen.blit(try_again_text, (try_again_button.centerx - try_again_text.get_width() // 2, try_again_button.centery - try_again_text.get_height() // 2))

    pygame.display.flip()

    return try_again_button

def reset_game():
    global score, grid
    score = 0
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile()
    add_random_tile()

def main():
    global score
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    
    add_random_tile()
    add_random_tile()
    draw_board(screen)
    
    game_over = False
    try_again_button = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:  # Restart the game
                        reset_game()
                        game_over = False
                        draw_board(screen)
                    continue
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = move('left')
                elif event.key == pygame.K_RIGHT:
                    moved = move('right')
                elif event.key == pygame.K_UP:
                    moved = move('up')
                elif event.key == pygame.K_DOWN:
                    moved = move('down')

                if moved:
                    add_random_tile()
                    draw_board(screen)

                if check_game_over():
                    game_over = True
                    try_again_button = show_game_over(screen)

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if try_again_button and try_again_button.collidepoint(event.pos):
                    reset_game()
                    game_over = False
                    draw_board(screen)

if __name__ == "__main__":
    main()
