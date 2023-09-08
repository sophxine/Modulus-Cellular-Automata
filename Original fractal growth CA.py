import pygame
import numpy as np

# Define constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 4
ITERATIONS = 5444444444444444
NUM_STATES = 2  # Number of cell states
MODULUS = 3     # Modulus for transition rules

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal Growth CA")

# Create an array to represent the grid of cells
grid = np.zeros((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE), dtype=int)

# Define the transition rules
def apply_rules(x, y):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = x + i, y + j
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                neighbors.append(grid[nx, ny])
    return sum(neighbors) % MODULUS

# Initialize the grid with a single active cell
grid[grid.shape[0] // 2, grid.shape[1] // 2] = 1

# Main loop
running = True
for _ in range(ITERATIONS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Create a copy of the grid to update in parallel
    new_grid = grid.copy()

    # Apply transition rules to update cell states
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            new_grid[x, y] = apply_rules(x, y)

    grid = new_grid

    # Visualization
    screen.fill((0, 0, 0))
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.flip()

pygame.quit()
