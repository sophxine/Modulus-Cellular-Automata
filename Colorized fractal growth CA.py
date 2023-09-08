import pygame
import numpy as np

# Define constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 3
ITERATIONS = 522
NUM_STATES = 2  # Number of cell states
MODULUS = 255   # Modulus for color mapping (range 0-255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal Growth CA")

# Create an array to represent the grid of cells
grid = np.zeros((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE), dtype=int)

# Define the transition rules
def apply_rules(grid):
    neighbors = np.roll(grid, (1, 1), (0, 1)) + np.roll(grid, (-1, -1), (0, 1)) + \
                np.roll(grid, (1, -1), (0, 1)) + np.roll(grid, (-1, 1), (0, 1)) + \
                np.roll(grid, (1, 0), (0, 1)) + np.roll(grid, (-1, 0), (0, 1)) + \
                np.roll(grid, (0, 1), (0, 1)) + np.roll(grid, (0, -1), (0, 1))

    return neighbors % MODULUS

# Initialize the grid with a single active cell
grid[grid.shape[0] // 2, grid.shape[1] // 2] = 1

# Create a backbuffer surface for rendering
backbuffer = pygame.Surface((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE))

# Main loop
running = True
for _ in range(ITERATIONS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply transition rules to update cell states
    neighbors = apply_rules(grid)
    grid = (grid + neighbors) % MODULUS

    # Create an RGB array from the grid
    colors = np.array([(r % 256, (r + 85) % 256, (r + 170) % 256) for r in grid.flat], dtype=np.uint8)
    colors = colors.reshape((grid.shape[0], grid.shape[1], 3))

    # Create a Pygame surface from the RGB array
    pygame.surfarray.blit_array(backbuffer, colors)

    # Scale up the backbuffer to match the screen dimensions
    backbuffer_scaled = pygame.transform.scale(backbuffer, (WIDTH, HEIGHT))

    # Blit the scaled backbuffer onto the screen
    screen.blit(backbuffer_scaled, (0, 0))
    pygame.display.flip()

pygame.quit()
