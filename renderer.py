import pygame

#dummy data for testing
R          = 15        
C          = 15        
CELL_SIZE  = 40        
WIDTH      = C * CELL_SIZE
HEIGHT     = R * CELL_SIZE
FPS        = 60
STEP_DELAY = 0.03

#dummy data for colors 
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (100, 200, 120)   
PURPLE = (130, 100, 220)   
BLUE   = (80,  140, 220)    
RED    = (220, 100,  80)   
GRAY   = (40,   40,  40) 


northWall = [[True] * C for _ in range(R)]
eastWall  = [[True] * C for _ in range(R)]
visited   = [[False] * C for _ in range(R)]

def cell_to_screen(row, col):
    """Convert maze (row, col) to top-left pixel (x, y)."""
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    return x, y


def draw_grid(screen):
    
    screen.fill(GRAY)
    for row in range(R):
        for col in range(C):
            x, y = cell_to_screen(row, col)
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
            pygame.draw.line(screen, WHITE,
                             (x + CELL_SIZE, y),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)
    pygame.draw.line(screen, WHITE, (0, 0), (0, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), 2)
    pygame.display.update()
