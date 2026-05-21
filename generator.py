# generator.py  —  Member 2
# Implements the DFS 'mouse' maze generation algorithm.

import random
import config

def generate_maze(draw_callback=None, delay_ms=15):
    """
    Generate a proper maze using iterative DFS (stack-based mouse).
    draw_callback: optional function called after each wall removal,
                   receives (mouse_r, mouse_c) for animation.
    """
    config.reset()

    # Place mouse at a random starting cell
    start_r = random.randint(0, config.R - 1)
    start_c = random.randint(0, config.C - 1)
    config.visited[start_r][start_c] = True

    stack = [(start_r, start_c)]  # the mouse's path history

    while stack:
        r, c = stack[-1]  # peek at top (current position)

        neighbors = config.get_unvisited_neighbors(r, c)

        if neighbors:
            # Pick a random unvisited neighbour
            nr, nc = random.choice(neighbors)

            # Eat through the wall between (r,c) and (nr,nc)
            config.remove_wall(r, c, nr, nc)

            # Mark new cell visited and push onto stack
            config.visited[nr][nc] = True
            stack.append((nr, nc))

            # Animate: tell the renderer to draw current state
            if draw_callback:
                draw_callback(nr, nc)
        else:
            # Dead end — backtrack by popping the stack
            stack.pop()

    # After maze is built, create start and end openings
    _create_openings()

def _create_openings():
    """Create entrance (left edge) and exit (right edge) openings."""
    # Start: random row, left edge (remove eastWall phantom column)
    sr = random.randint(0, config.R - 1)
    config.eastWall[sr][0] = 0          # gap in left edge
    config.start_cell = (sr, 0)

    # End: random row, right edge (remove eastWall at column C)
    er = random.randint(0, config.R - 1)
    config.eastWall[er][config.C] = 0   # gap in right edge
    config.end_cell = (er, config.C - 1)


