import pygame
import random
import sys

# ----- Initialize -----
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10  # Initial speed

# ----- Colors -----
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# ----- Setup -----
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

# ----- Snake / Apple -----
snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)  # moving right
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0
game_over = False

# ----- Draw Functions -----
def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARKGREEN, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARKGREEN, (0, y), (WIDTH, y))

# ----- Main Loop -----
while True:
    screen.fill(BLACK)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control snake
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_r and game_over:
                # Restart
                snake = [(10, 10), (9, 10), (8, 10)]
                direction = (1, 0)
                apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                score = 0
                FPS = 10
                game_over = False

    if not game_over:
        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (
            head in snake
            or head[0] < 0 or head[0] >= GRID_WIDTH
            or head[1] < 0 or head[1] >= GRID_HEIGHT
        ):
            game_over = True
        else:
            snake.insert(0, head)
            if head == apple:
                score += 1
                FPS += 1  # 🧠 Increase speed per apple
                while True:
                    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                    if apple not in snake:
                        break
            else:
                snake.pop()

    # Draw apple and snake
    draw_cell(apple, RED)
    for segment in snake:
        draw_cell(segment, GREEN)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        msg = font.render("Game Over! Press R to restart", True, RED)
        screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)
