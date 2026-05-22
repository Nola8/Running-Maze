import random
import config

def generate_maze(draw_callback=None, delay_ms=15):
    config.reset()

    start_r = random.randint(0, config.R - 1)
    start_c = random.randint(0, config.C - 1)
    config.visited[start_r][start_c] = True

    stack = [(start_r, start_c)]

    while stack:
        r, c = stack[-1]

        neighbors = config.get_unvisited_neighbors(r, c)

        if neighbors:
            nr, nc = random.choice(neighbors)
            config.remove_wall(r, c, nr, nc)
            config.visited[nr][nc] = True
            stack.append((nr, nc))
            if draw_callback:
                draw_callback(nr, nc)
        else:
            stack.pop()
    _create_openings()

def _create_openings():
    sr = random.randint(0, config.R - 1)
    config.eastWall[sr][0] = 0
    config.start_cell = (sr, 0)

    er = random.randint(0, config.R - 1)
    config.eastWall[er][config.C] = 0
    config.end_cell = (er, config.C - 1)


