import pygame
import config

def cell_to_screen(row, col):
    x = config.MARGIN + col * config.CELL_SIZE
    y = config.MARGIN + (config.R - 1 - row) * config.CELL_SIZE
    return x, y



def draw_grid(screen):
    screen.fill(config.BG_COLOR)
    for row in range(config.R):
        for col in range(config.C):
            x, y = cell_to_screen(row, col)
            pygame.draw.rect(screen, config.WALL_COLOR,
                             (x,y, config.CELL_SIZE, config.CELL_SIZE), 1)

def draw_maze(screen):
    screen.fill(config.BG_COLOR)

    pygame.draw.rect(screen, config.WALL_COLOR, (
        config.MARGIN, config.MARGIN,
        config.C * config.CELL_SIZE,
        config.R * config.CELL_SIZE), 2)

    for r in range(config.R):
        for c in range(config.C):
            x, y = cell_to_screen(r, c)

            if config.northWall[r + 1][c]:   # r+1 because phantom row
                pygame.draw.line(screen, config.WALL_COLOR,
                    (x, y), (x + config.CELL_SIZE, y), 2)

            if config.eastWall[r][c + 1]:
                pygame.draw.line(screen, config.WALL_COLOR,
                    (x + config.CELL_SIZE, y),
                    (x + config.CELL_SIZE, y + config.CELL_SIZE), 2)

    _draw_openings(screen)

def _draw_openings(screen):
    if config.start_cell:
        r, c = config.start_cell
        x, y = cell_to_screen(r, c)
        pygame.draw.line(screen, config.BG_COLOR,
            (x, y + 2), (x, y + config.CELL_SIZE - 2), 3)
        pygame.draw.circle(screen, config.ORANGE,
            (x + config.CELL_SIZE//4, y + config.CELL_SIZE//2), 6)

    if config.end_cell:
        r, c = config.end_cell
        x, y = cell_to_screen(r, c)
        rx = x + config.CELL_SIZE
        pygame.draw.line(screen, config.BG_COLOR,
            (rx, y + 2), (rx, y + config.CELL_SIZE - 2), 3)
        pygame.draw.circle(screen, config.ORANGE,
            (rx - config.CELL_SIZE//4, y + config.CELL_SIZE//2), 6)

def draw_cell_color(screen, r, c, color):
    x, y = cell_to_screen(r, c)
    inner = config.CELL_SIZE - 4
    pygame.draw.rect(screen, color, (x + 2, y + 2, inner, inner))

def draw_dot(screen, r, c, color, radius=None):
    if radius is None:
        radius = config.CELL_SIZE // 2 - 4
    x, y = cell_to_screen(r, c)
    cx = x + config.CELL_SIZE // 2
    cy = y + config.CELL_SIZE // 2
    pygame.draw.circle(screen, color, (cx, cy), radius)

