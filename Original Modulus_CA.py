# Left mouse button = Draw
# Space = Pause and resume
# You can experiment with changing the rules in apply_rules


import pygame
import numpy as np

# Define constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 4
ITERATIONS = 0

NUM_STATES = 2  # Number of cell states
MODULUS = 255   # Modulus for color mapping (range 0-255)

DEATH_MODULUS = 10  # Initial modulus for cell death (Not working)
CONSERVATISM = 1  # Conservatism factor (adjust as needed)
NEIGHBOR_THRESHOLD = 312  # Threshold for cell death based on neighbors
TRANSLATIONAL_DISTANCE = 1  # Fixed distance for translational symmetry

DRAW_COLOR = (255, 255, 255)  # Color for drawing

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modulus CA")

# Create an array to represent the grid of cells
grid = np.zeros((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE), dtype=int)

# Create a boolean array to track the drawing state and pause state
drawing = False
paused = False
allow_pause_while_drawing = True  # Option to allow pausing while drawing (Not working)
space_pressed = False  # Track if the spacebar is pressed

# Keep track of the current drawing position
current_draw_position = None

# Define the transition rules with translational and rotational symmetry, conservativism, and cell death
def apply_rules(grid):
    neighbors = (
        np.roll(grid, (1, 0), (0, 1)) +
        np.roll(grid, (-1, 0), (0, 1)) +
        np.roll(grid, (0, 1), (0, 1)) +
        np.roll(grid, (0, -1), (0, 1))
    )

    # Apply translational symmetry
    for i in range(1, TRANSLATIONAL_DISTANCE + 1):
        neighbors += (
            np.roll(grid, (i, 0), (0, 1)) +
            np.roll(grid, (-i, 0), (0, 1)) +
            np.roll(grid, (0, i), (0, 1)) +
            np.roll(grid, (0, -i), (0, 1))
        )

    # Apply 90-degree rotational symmetry
    neighbors_rotated = (
        np.roll(grid, (0, 1), (0, 1)) +
        np.roll(grid, (1, 0), (0, 1)) +
        np.roll(grid, (0, -1), (0, 1)) +
        np.roll(grid, (-1, 0), (0, 1))
    )

    new_grid = (grid + neighbors + neighbors_rotated) % MODULUS

    # Apply cell death rule based on neighborhood count
    death_mask = (neighbors >= NEIGHBOR_THRESHOLD)
    new_grid = np.where(death_mask, 0, new_grid)

    # Apply conservativism
    change_mask = (np.random.rand(*new_grid.shape) < CONSERVATISM)
    return np.where(change_mask, new_grid, grid)

# Function to draw on the grid with boundary checks
def draw_on_grid(grid, pos):
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

    # Check if the grid coordinates are within bounds
    if 0 <= grid_x < grid.shape[0] and 0 <= grid_y < grid.shape[1]:
        grid[grid_x, grid_y] = 1

# Create a backbuffer surface for rendering
backbuffer = pygame.Surface((WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                current_draw_position = event.pos
                draw_on_grid(grid, current_draw_position)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                drawing = False
                current_draw_position = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                new_draw_position = event.pos
                if new_draw_position != current_draw_position:
                    draw_on_grid(grid, new_draw_position)
                    current_draw_position = new_draw_position
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True  # Spacebar is pressed
                paused = not paused  # Toggle pause state
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False  # Spacebar is released

    # Check if pausing is allowed while drawing
    if allow_pause_while_drawing:
        if not paused and not drawing and space_pressed:
            paused = True  # Pause when spacebar is pressed
        elif paused and drawing and not space_pressed:
            paused = False  # Resume when spacebar is released

    # If not paused, apply transition rules to update cell states
    if not paused:
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
