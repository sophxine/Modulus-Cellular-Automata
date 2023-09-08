import pygame
import numpy as np

# Define constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 4
ITERATIONS = 544
NUM_STATES = 2  # Number of cell states
MODULUS = 255   # Modulus for color mapping (range 0-255)
CONSERVATISM = 1  # Conservatism factor (Change to 0.1 for a growing plant-like pattern)
DEATH_MODULUS = 3  # Modulus for cell death (adjust as needed)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stable Fractal Growth CA")

# Create an array to represent the grid of cells
grid = np.zeros((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE), dtype=int)

# Define the transition rules with conservativism and cell death
def apply_rules(grid):
    neighbors = np.roll(grid, (1, 1), (0, 1)) + np.roll(grid, (-1, -1), (0, 1)) + \
                np.roll(grid, (1, -1), (0, 1)) + np.roll(grid, (-1, 1), (0, 1)) + \
                np.roll(grid, (1, 0), (0, 1)) + np.roll(grid, (-1, 0), (0, 1)) + \
                np.roll(grid, (0, 1), (0, 1)) + np.roll(grid, (0, -1), (0, 1))

    new_grid = (grid + neighbors) % MODULUS

    # Apply cell death rule
    death_mask = (new_grid % DEATH_MODULUS == 0)
    new_grid = np.where(death_mask, 0, new_grid)

    # Apply conservativism
    change_mask = (np.random.rand(*new_grid.shape) < CONSERVATISM)
    return np.where(change_mask, new_grid, grid)

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
    grid = apply_rules(grid)

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
