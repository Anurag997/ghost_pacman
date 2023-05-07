import pygame
import random

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
DOT_SIZE = 5
DOT_COLOR = (255, 255, 255)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
PACMAN_SPEED = 2
GHOST_SPEED = 3

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ghost Pac-Man')

# Create the grid with dots
grid = [['.' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Place Pac-Man randomly on the grid
pacman_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
grid[pacman_position[1]][pacman_position[0]] = 'P'

# Place the ghost randomly on the grid
ghost_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
while ghost_position == pacman_position:
    ghost_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
grid[ghost_position[1]][ghost_position[0]] = 'G'

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == '.':
                pygame.draw.circle(screen, DOT_COLOR, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), DOT_SIZE)
            elif grid[y][x] == 'P':
                pygame.draw.circle(screen, PACMAN_COLOR, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
            elif grid[y][x] == 'G':
                pygame.draw.rect(screen, GHOST_COLOR, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def move_pacman():
    global pacman_position
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = pacman_position[0] + dx, pacman_position[1] + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and grid[new_y][new_x] != 'G':
            grid[pacman_position[1]][pacman_position[0]] = '.'
            pacman_position = (new_x, new_y)
            grid[new_y][new_x] = 'P'
            break

def move_ghost(direction):
    global ghost_position
    dx, dy = direction
    new_x, new_y = ghost_position[0] + dx, ghost_position[1] + dy
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        grid[ghost_position[1]][ghost_position[0]] = '.'
        ghost_position = (new_x, new_y)
        grid[new_y][new_x] = 'G'

def count_dots():
    return sum(row.count('.') for row in grid)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_ghost((0, -1))
            elif event.key == pygame.K_DOWN:
                move_ghost((0, 1))
            elif event.key == pygame.K_LEFT:
                move_ghost((-1, 0))
            elif event.key == pygame.K_RIGHT:
                move_ghost((1, 0))

    # Update Pac-Man
    move_pacman()

    # Check for collisions
    if pacman_position == ghost_position:
        print("You won!")
        running = False
    elif count_dots() == 0:
        print("You lost!")
        running = False

    # Draw the grid
    screen.fill((0, 0, 0))
    draw_grid()

    # Update the screen
    pygame.display.update()
    pygame.time.delay(200)

# Clean up
pygame.quit()
