import pygame

#dummy data for testing
R          = 15        
C          = 15        
CELL_SIZE  = 40        
WIDTH      = C * CELL_SIZE
HEIGHT     = R * CELL_SIZE
FPS        = 60
STEP_DELAY = 0.03


northWall = [[True] * C for _ in range(R)]
eastWall  = [[True] * C for _ in range(R)]
visited   = [[False] * C for _ in range(R)]

def cell_to_screen(row, col):
    """Convert maze (row, col) to top-left pixel (x, y)."""
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    return x, y

