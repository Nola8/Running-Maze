import pygame
import time

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

def draw_start_end(screen):
    
    start_y = 0
    pygame.draw.line(screen, GRAY,
                     (0, start_y + 2),
                     (0, start_y + CELL_SIZE - 2), 4)
 
    end_x = (C - 1) * CELL_SIZE
    pygame.draw.line(screen, GRAY,
                     (end_x + 2, HEIGHT),
                     (end_x + CELL_SIZE - 2, HEIGHT), 4)
 
    font = pygame.font.SysFont(None, 20)
    screen.blit(font.render("S", True, BLUE),  (4, 4))
    screen.blit(font.render("E", True, RED),
                ((C - 1) * CELL_SIZE + 4, (R - 1) * CELL_SIZE + 4))

def draw_maze(screen, mouse_row=None, mouse_col=None):
    
    screen.fill(GRAY)
 
    for row in range(R):
        for col in range(C):
            if not visited[row][col]:
                continue
            x, y = cell_to_screen(row, col)
            if row == 0 and col == 0:
                colour = BLUE
            elif row == R - 1 and col == C - 1:
                colour = RED 
            else:
                colour = GREEN
            pygame.draw.rect(screen, colour,
                             (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
 
    if mouse_row is not None:
        x, y = cell_to_screen(mouse_row, mouse_col)
        pygame.draw.rect(screen, PURPLE,
                         (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        pygame.draw.circle(screen, WHITE, (cx, cy), CELL_SIZE // 6)
 
    for row in range(R):
        for col in range(C):
            x, y = cell_to_screen(row, col)
 
            if northWall[row][col]:
                pygame.draw.line(screen, WHITE,
                                 (x, y), (x + CELL_SIZE, y), 2)
 
            if eastWall[row][col]:
                pygame.draw.line(screen, WHITE,
                                 (x + CELL_SIZE, y),
                                 (x + CELL_SIZE, y + CELL_SIZE), 2)
 
    pygame.draw.line(screen, WHITE, (0, 0), (0, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), 2)
 
    draw_start_end(screen)
 
    pygame.display.update()

def erase_wall_effect(screen, row, col, direction):
    x, y = cell_to_screen(row, col)
 
    if direction == 'N':
        pygame.draw.line(screen, GRAY, (x + 1, y), (x + CELL_SIZE - 1, y), 3)
    elif direction == 'E':
        pygame.draw.line(screen, GRAY,
                         (x + CELL_SIZE, y + 1),
                         (x + CELL_SIZE, y + CELL_SIZE - 1), 3)
    elif direction == 'S':
        ny = y + CELL_SIZE
        pygame.draw.line(screen, GRAY, (x + 1, ny), (x + CELL_SIZE - 1, ny), 3)
    elif direction == 'W':
        pygame.draw.line(screen, GRAY,
                         (x, y + 1), (x, y + CELL_SIZE - 1), 3)
 
    pygame.display.update()
    time.sleep(STEP_DELAY)        
