import pygame
import config
import renderer

clock = None
screen = None
GENERATION_SPEED = 30   # milliseconds between generation frames
SOLVE_SPEED      = 20   # milliseconds between solve frames

def init():
    global clock, screen
    pygame.init()
    screen = pygame.display.set_mode((config.WIN_W, config.WIN_H))
    pygame.display.set_caption('Building and Running Mazes')
    clock = pygame.time.Clock()
    screen.fill(config.BG_COLOR)
    pygame.display.flip()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True

def generation_frame(mouse_r, mouse_c):
    if not handle_events():
        pygame.quit()
        raise SystemExit

    renderer.draw_maze(screen)
    renderer.draw_dot(screen, mouse_r, mouse_c, config.GREEN)
    pygame.display.flip()
    pygame.time.delay(GENERATION_SPEED)

def solve_frame(path, dead_cells):
    if not handle_events():
        pygame.quit()
        raise SystemExit

    renderer.draw_maze(screen)

    for r, c in dead_cells:
        renderer.draw_cell_color(screen, r, c, config.BLUE)

    for r, c in path:
        renderer.draw_dot(screen, r, c, config.RED, radius=4)

    if path:
        mr, mc = path[-1]
        renderer.draw_dot(screen, mr, mc, config.GREEN)

    pygame.display.flip()
    pygame.time.delay(SOLVE_SPEED)

def show_solution(solution_path):
    """Highlight the final solution path after solving is complete."""
    renderer.draw_maze(screen)
    for r, c in solution_path:
        renderer.draw_cell_color(screen, r, c, (255, 200, 200))
        renderer.draw_dot(screen, r, c, config.RED, radius=4)
    pygame.display.flip()

def wait_for_quit():
    """Keep window open until user closes it."""
    while True:
        if not handle_events():
            break
        clock.tick(30)
    pygame.quit()
