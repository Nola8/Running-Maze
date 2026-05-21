
#Grid Dimensions Row and Column
R = 12
C = 18

# Display Constants 

CELL_SIZE = 40
MARGIN = 20
WIN_W = C * CELL_SIZE + 2 * MARGIN
WIN_H = R * CELL_SIZE + 2 * MARGIN

# Colors
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = ( 34, 177,  76)   # mouse / active cell
RED        = (220,  50,  50)   # solver path
BLUE       = ( 66, 133, 244)   # dead-end cells
ORANGE     = (230, 126,  34)   # start / end markers
WALL_COLOR = (  0,   0,   0)   # maze walls
BG_COLOR   = (255, 255, 255)   # background

# Wall arrays
northWall = [[1] * C for _ in range(R + 1)]
eastWall  = [[1] * (C + 1) for _ in range(R)]

# Visited tracking
visited = [[False] * C for _ in range(R)]

# Start and end cells
start_cell = None   # [row, 0]  — left edge
end_cell   = None   # [row, C-1] — right edge


