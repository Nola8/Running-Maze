# solver.py  —  Member 4
# Backtracking DFS maze solver.

import config

def solve_maze(draw_callback=None):
    """
    Solve the maze using iterative backtracking DFS.
    draw_callback: optional function(stack, dead_cells) called each step.
    Returns: list of (r,c) tuples representing the solution path,
             or None if no path exists.
    """
    if not config.start_cell or not config.end_cell:
        raise RuntimeError('Maze not generated yet. Run generator first.')

    sr, sc = config.start_cell
    er, ec = config.end_cell

    # Track which cells the solver has visited
    solve_visited = [[False] * config.C for _ in range(config.R)]
    solve_visited[sr][sc] = True

    stack = [(sr, sc)]      # current path (also the solve stack)
    dead_cells = set()      # cells that led to dead ends (drawn blue)

    while stack:
        r, c = stack[-1]

        # SUCCESS: reached the end
        if r == er and c == ec:
            if draw_callback:
                draw_callback(list(stack), dead_cells)
            return list(stack)   # the solution path

        moved = False
        for direction in ['N', 'E', 'S', 'W']:
            nr, nc = _neighbor(r, c, direction)
            if nr is None:
                continue
            if config.can_move(r, c, direction) and not solve_visited[nr][nc]:
                solve_visited[nr][nc] = True
                stack.append((nr, nc))
                moved = True
                break   # move one step at a time for animation

        if not moved:
            # Dead end — backtrack
            dead_cells.add((r, c))
            stack.pop()

        if draw_callback:
            draw_callback(list(stack), dead_cells)

    return None   # no solution (should not happen in a proper maze)

def _neighbor(r, c, direction):
    """Return (nr, nc) for the cell in the given direction, or (None,None)."""
    if direction == 'N' and r + 1 < config.R:  return r + 1, c
    if direction == 'S' and r - 1 >= 0:        return r - 1, c
    if direction == 'E' and c + 1 < config.C:  return r, c + 1
    if direction == 'W' and c - 1 >= 0:        return r, c - 1
    return None, None

