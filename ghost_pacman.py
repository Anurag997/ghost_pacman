import pygame
import random

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
MAZE = [
    '####################',
    '#..................#',
    '#.####.#####.####.#',
    '#.#  #.#   #.# #.#',
    '#.#..#.###.#.##.#.#',
    '#.#  #.#   #.#  #.#',
    '#.####.#####.####.#',
    '#..................#',
    '####################'
]
GHOST_SPEED = 3
GHOST_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
GHOST_START_POSITIONS = [(SCREEN_WIDTH // 2 - BLOCK_SIZE, SCREEN_HEIGHT // 2 - BLOCK_SIZE),
                         (SCREEN_WIDTH // 2 + BLOCK_SIZE, SCREEN_HEIGHT // 2 - BLOCK_SIZE),
                         (SCREEN_WIDTH // 2 - BLOCK_SIZE, SCREEN_HEIGHT // 2 + BLOCK_SIZE),
                         (SCREEN_WIDTH // 2 + BLOCK_SIZE, SCREEN_HEIGHT // 2 + BLOCK_SIZE)]
PACMAN_SPEED = 5
PACMAN_START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
PACMAN_START_DIRECTION = 'left'

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ghost Pac-Man')

# Set up the font
font = pygame.font.SysFont('Arial', 20)

# Define function for drawing the maze
def draw_maze():
    for y in range(len(MAZE)):
        for x in range(len(MAZE[y])):
            if MAZE[y][x] == '#':
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Define the Ghost class
class Ghost:
    def __init__(self, color, start_position):
        self.color = color
        self.rect = pygame.Rect(start_position[0], start_position[1], BLOCK_SIZE, BLOCK_SIZE)
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def update(self):
        # Move the ghost in its current direction
        if self.direction == 'up':
            self.rect.y -= GHOST_SPEED
        elif self.direction == 'down':
            self.rect.y += GHOST_SPEED
        elif self.direction == 'left':
            self.rect.x -= GHOST_SPEED
        elif self.direction == 'right':
            self.rect.x += GHOST_SPEED

        # Check for collisions with walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
        elif self.rect.left % BLOCK_SIZE == 0 and self.rect.top % BLOCK_SIZE == 0:
            if self.rect.left // BLOCK_SIZE < 0 or self.rect.left // BLOCK_SIZE >= len(MAZE[0]) or self.rect.top // BLOCK_SIZE < 0 or self.rect.top // BLOCK_SIZE >= len(MAZE) or MAZE[self.rect.top // BLOCK_SIZE][self.rect.left // BLOCK_SIZE] == '#' or MAZE[self.rect.bottom // BLOCK_SIZE][self.rect.right // BLOCK_SIZE] == '#' or MAZE[self.rect.top // BLOCK_SIZE][self.rect.right // BLOCK_SIZE] == '#' or MAZE[self.rect.bottom // BLOCK_SIZE][self.rect.left // BLOCK_SIZE] == '#':
                self.direction = random.choice(['up', 'down', 'left', 'right'])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Define the Pac-Man class
class Pacman:
    def __init__(self, start_position, start_direction):
        self.rect = pygame.Rect(start_position[0], start_position[1], BLOCK_SIZE, BLOCK_SIZE)
        self.direction = start_direction

    def update(self):
        # Move Pac-Man in its current direction
        if self.direction == 'up':
            self.rect.y -= PACMAN_SPEED
        elif self.direction == 'down':
            self.rect.y += PACMAN_SPEED
        elif self.direction == 'left':
            self.rect.x -= PACMAN_SPEED
        elif self.direction == 'right':
            self.rect.x += PACMAN_SPEED

        # Check for collisions with walls
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.left % BLOCK_SIZE == 0 and self.rect.top % BLOCK_SIZE == 0:
            if self.rect.left // BLOCK_SIZE < 0 or self.rect.left // BLOCK_SIZE >= len(MAZE[0]) or self.rect.top // BLOCK_SIZE < 0 or self.rect.top // BLOCK_SIZE >= len(MAZE) or MAZE[self.rect.top // BLOCK_SIZE][self.rect.left // BLOCK_SIZE] == '#' or MAZE[self.rect.bottom // BLOCK_SIZE][self.rect.right // BLOCK_SIZE] == '#' or MAZE[self.rect.top // BLOCK_SIZE][self.rect.right // BLOCK_SIZE] == '#' or MAZE[self.rect.bottom // BLOCK_SIZE][self.rect.left // BLOCK_SIZE] == '#':
                if self.direction == 'up':
                    self.rect.top = (self.rect.top // BLOCK_SIZE) * BLOCK_SIZE
                elif self.direction == 'down':
                    self.rect.bottom = ((self.rect.bottom - 1) // BLOCK_SIZE + 1) * BLOCK_SIZE
                elif self.direction == 'left':
                    self.rect.left = (self.rect.left // BLOCK_SIZE) * BLOCK_SIZE
                elif self.direction == 'right':
                    self.rect.right = ((self.rect.right - 1) // BLOCK_SIZE + 1) * BLOCK_SIZE

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.rect.centerx, self.rect.centery), BLOCK_SIZE // 2)

# Create the ghosts
ghosts = []
for i in range(len(GHOST_COLORS)):
    ghosts.append(Ghost(GHOST_COLORS[i], GHOST_START_POSITIONS[i]))

# Create Pac-Man
pacman = Pacman(PACMAN_START_POSITION, PACMAN_START_DIRECTION)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.direction = 'up'
            elif event.key == pygame.K_DOWN:
                pacman.direction = 'down'
            elif event.key == pygame.K_LEFT:
                pacman.direction = 'left'
            elif event.key == pygame.K_RIGHT:
                pacman.direction = 'right'

    # Update the ghosts
    for ghost in ghosts:
        ghost.update()

    # Update Pac-Man
    pacman.update()

    # Draw the maze
    draw_maze()

    # Draw the ghosts
    for ghost in ghosts:
        ghost.draw()

    # Draw Pac-Man
    pacman.draw()

    # Check for collisions with ghosts
    for ghost in ghosts:
        if pacman.rect.colliderect(ghost.rect):
            text = font.render('Game Over', True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() //2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

    # Update the screen
    pygame.display.update()

# Clean up
pygame.quit()
