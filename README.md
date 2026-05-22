# Running Maze

## Table of Contents

1. [Project Overview](#-project-overview)
2. [How It Works](#-how-it-works)
   - [Part A: Maze Generation (DFS Mouse)](#part-a--maze-generation-dfs-mouse)
   - [Part B: Maze Solver (Backtracking)](#part-b--maze-solver-backtracking)
   - [Data Structure](#data-structure)
3. [Bonus: Cycles & the Shoulder-to-the-Wall Rule](#-bonus--cycles--the-shoulder-to-the-wall-rule)
4. [Project Structure](#-project-structure)
5. [Installation & Dependencies](#-installation--dependencies)
6. [Running the Program](#-running-the-program)
7. [Controls](#-controls)
8. [Visual Legend](#-visual-legend)
9. [Troubleshooting](#-troubleshooting)
10. [Team & Contributions](#-team--contributions)
11. [Loom Recording](#-loom-recording)
12. [Discussion — Stack vs Queue](#-discussion--stack-vs-queue)

---

## Project Overview

This program fulfils the two core requirements from the assignment paper:

| Requirement | Description |
|---|---|
| **Generate** | Build a rectangular maze of **R rows × C columns**, displayed dynamically as walls are carved |
| **Solve** | Find and display the path from the **left-edge opening** to the **right-edge opening** |

Every maze produced is **proper**: every one of the R × C cells is connected by a unique, albeit tortuous, path to every other cell. This is guaranteed by the spanning-tree property of the DFS generation algorithm.

---

## ⚙️ How It Works

### Part 1: Maze Generation (DFS Mouse)

The maze starts as a full grid — every cell has all four walls intact. An invisible **"mouse"** is placed at a randomly chosen starting cell and tasked with eating through walls to connect adjacent cells.

**Algorithm (iterative DFS with a stack):**

```
1. Place mouse at a random cell. Mark it visited. Push onto stack.
2. Peek at the top of the stack (current position).
3. Find all 4 neighbours that are UNVISITED (all four walls still intact).
4. If unvisited neighbours exist:
       → Pick one randomly
       → Eat through the connecting wall (set northWall or eastWall to 0)
       → Mark the new cell visited
       → Push the new cell onto the stack
5. If no unvisited neighbours (dead end):
       → Pop the stack (backtrack to previous cell)
6. Repeat from step 2 until the stack is empty.
   When the stack is empty → every cell has been visited → maze is complete.
7. Choose a random row on the LEFT edge (start) and RIGHT edge (end).
   Remove the corresponding wall to create the entry and exit openings.
```

The result is a **spanning tree** — a connected graph with no cycles, meaning there is exactly one path between any two cells.

>  It is *delightful* to watch the maze being formed dynamically as the mouse eats through walls, which is why the generation is fully animated frame-by-frame.

---

### Part 2: Maze Solver (Backtracking)

Once the maze is generated, a second mouse traverses it using a **backtracking DFS** algorithm.

**Algorithm:**

```
1. Start at the left-edge opening. Mark it visited. Push onto solve stack.
2. Try to move in a direction (N/E/S/W) where:
       → There is NO wall blocking the path (northWall or eastWall = 0)
       → The destination cell has NOT been visited
3. If a valid move exists:
       → Push new position onto stack
       → Draw the mouse position as a RED dot
4. If no valid moves (dead end):
       → Mark the current cell BLUE
       → Pop the stack (backtrack)
       → Optionally re-raise the wall to the dead-end cell
5. Repeat until the mouse reaches the right-edge opening.
6. The solve stack at termination contains the SOLUTION PATH.
```

---

### Data Structure

The maze is represented exactly as specified in the assignment:

```python
# northWall[r][c] = 1  →  the top wall of cell (r, c) is intact
# northWall[r][c] = 0  →  the wall has been removed (eaten through)
#
# Row 0 is a PHANTOM ROW of cells below the maze.
# Its north walls form the BOTTOM EDGE of the maze.
northWall = [[1] * C for _ in range(R + 1)]

# eastWall[r][c] = 1  →  the right wall of cell (r, c) is intact
# eastWall[r][c] = 0  →  the wall has been removed
#
# eastWall[r][0] specifies where gaps appear in the LEFT EDGE of the maze.
eastWall = [[1] * (C + 1) for _ in range(R)]
```

**Key boundary rules:**
- `northWall[0][c]` — bottom edge of the visible maze (phantom row)
- `eastWall[r][0]` — left edge of the maze; setting to `0` creates the start opening
- `eastWall[r][C]` — right edge of the maze; setting to `0` creates the end opening

**Wall removal logic:**

```python
def remove_wall(r1, c1, r2, c2):
    """Remove the wall between adjacent cells (r1,c1) and (r2,c2)."""
    if r2 == r1 + 1:      # neighbour is above
        northWall[r1 + 1][c1] = 0
    elif r2 == r1 - 1:    # neighbour is below
        northWall[r1][c1] = 0
    elif c2 == c1 + 1:    # neighbour is to the right
        eastWall[r1][c1 + 1] = 0
    elif c2 == c1 - 1:    # neighbour is to the left
        eastWall[r1][c1] = 0
```

---

## Bonus point: Cycles & the Shoulder-to-the-Wall Rule

### The Addendum Implemention

As described in the assignment Addendum, proper mazes are actually not too challenging because you can always solve them using the **"shoulder-to-the-wall"** rule:

> Trace the maze by rubbing your shoulder along the left-hand wall. At a dead end, sweep around and retrace the path, always maintaining contact with the wall. Because the maze is a tree, you will always reach your destination.

This works on proper mazes because they contain **no cycles** — they are spanning trees. The shoulder-to-the-wall rule guarantees success when both start and end cells are on the outer boundary.

### Breaking the Rule

To make things more challenging, we implemented the bonus feature: **after generating the proper maze, the mouse eats approximately 1 in every 20 remaining intact interior walls at random.**

```python
def add_bonus_cycles(probability=0.05):
    """
    Remove extra walls randomly to create cycles in the maze.
    This breaks the shoulder-to-the-wall traversal guarantee.
    Default: ~1 in 20 intact walls are removed.
    """
    for r in range(R):
        for c in range(C - 1):
            if eastWall[r][c + 1] == 1:       # wall still intact
                if random.random() < probability:
                    eastWall[r][c + 1] = 0    # eat it
```

**Why this defeats the shoulder-to-the-wall rule:**

When extra walls are removed, **cycles are introduced** into the maze graph. These cycles can form closed loops that encircle the exit cell. A solver following the wall blindly will loop indefinitely around the cycle, never detecting that the exit is enclosed inside the loop. The backtracking DFS solver in this program is **not affected** — it tracks visited cells and cannot get caught in a cycle.

To enable the bonus mode, uncomment this line in `main.py`:

```python
# add_bonus_cycles(0.05)   ← uncomment to enable bonus cycles
```

---

## Project Structure

```
maze_project/
│
├── main.py          # Entry point — wires all modules together
├── config.py        # northWall / eastWall arrays, constants, shared utilities
├── generator.py     # DFS mouse maze generation algorithm
├── renderer.py      # pygame wall drawing and coordinate conversion
├── solver.py        # Backtracking DFS maze solver
├── animator.py      # Animation loop, frame callbacks, dot rendering
│
└── README.md        # This file
```

**Module dependency map:**

```
main.py
  ├── config.py       (no dependencies)
  ├── generator.py    (imports config)
  ├── renderer.py     (imports config, pygame)
  ├── solver.py       (imports config)
  └── animator.py     (imports config, renderer, pygame)
```

---

## Installation & Dependencies

### Requirements

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.10 or higher | Runtime |
| pygame | 2.x | Window, graphics, animation |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_TEAM/maze-assignment.git
cd maze-assignment
```

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

> Using a virtual environment keeps pygame isolated from your system Python and prevents version conflicts.

### Step 3 — Install pygame

```bash
pip install pygame
```

To confirm it installed correctly:

```bash
python -c "import pygame; print(pygame.version.ver)"
# Expected output: 2.x.x
```

### Step 4 — Verify Python Version

```bash
python --version
# Must be 3.10 or higher
```

---

## Running the Program

```bash
# Make sure your virtual environment is active, then:
python main.py
```

The program will:
1. Open a pygame window and draw the full initial grid
2. Animate the DFS mouse carving the maze (green dot)
3. Pause briefly so you can see the completed maze
4. Animate the backtracking solver (red path, blue dead ends)
5. Highlight the final solution path
6. Keep the window open until you press `ESC` or close it

### Adjusting Maze Size and Speed

Open `config.py` and change these values:

```python
R = 12          # number of rows  (try 5–30)
C = 18          # number of columns (try 5–40)
CELL_SIZE = 40  # pixels per cell (reduce for larger mazes)
```

Open `animator.py` to change animation speed:

```python
GENERATION_SPEED = 30   # ms between generation frames (lower = faster)
SOLVE_SPEED      = 20   # ms between solve frames (lower = faster)
```

---

## Controls

| Key / Action | Effect |
|---|---|
| `ESC` | Close the window |
| Close button (×) | Exit the program |

---

## Visual 

| Colour | Meaning |
|---|---|
| **Green dot** | Mouse's current position during generation or solving |
| **Red dot / fill** | Current solution path being explored by the solver |
| **Blue fill** | Dead-end cell — solver has backtracked from here |
| **Orange marker** | Start cell (left edge) and end cell (right edge) |
| **Black lines** | Intact walls |
| **White / gap** | Removed wall (passage) |

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'pygame'`

pygame is not installed in the current environment.

```bash
pip install pygame
```

If you have multiple Python versions, make sure you are using the right pip:

```bash
python -m pip install pygame
```

---

### `ModuleNotFoundError: No module named 'config'`

You are not running from the project root directory.

```bash
# Make sure you are inside the maze_project folder
cd maze_project
python main.py
```

---

### Black window appears but nothing draws

The pygame display is not being flushed. Check that `pygame.display.flip()` is called after every draw operation in `animator.py`. Also confirm `animator.init()` is being called before any rendering.

---

### Walls are not being removed during generation

The `remove_wall()` function in `config.py` may have swapped `r1`/`r2` or `c1`/`c2` arguments. Double-check that the call in `generator.py` passes `(current_row, current_col, neighbour_row, neighbour_col)` in that order.

---

### Maze is not proper (isolated cells or multiple paths between two cells)

The `visited[][]` array is not being reset between runs. Call `config.reset()` at the start of each new generation. Also check that `get_unvisited_neighbors()` correctly reads from `visited[][]` and not from a stale local copy.

---

### The solver loops forever / never reaches the exit

The solver's `solve_visited[][]` array is shared or not being initialised fresh per run. Make sure it is declared inside `solve_maze()` and not at module level. Also verify `can_move()` is checking the correct `northWall` / `eastWall` index for each direction.

---

### Animation is too slow / too fast

Change the delay values in `animator.py`:

```python
GENERATION_SPEED = 30   # increase to slow down, decrease to speed up
SOLVE_SPEED      = 20   # same
```

Set either to `1` for near-instant generation (useful when debugging).

---

### `pygame.error: No available video device`

This happens when running on a headless server (no display). pygame requires a display. Run the program on a local machine, or set up a virtual display:

```bash
# Linux only — install a virtual display
sudo apt-get install xvfb
Xvfb :99 -screen 0 1024x768x24 &
DISPLAY=:99 python main.py
```

---

### Window opens then immediately closes

An unhandled exception is crashing the program before the event loop starts. Run from a terminal (not by double-clicking) so you can see the full error traceback:

```bash
python main.py
```

---

##  Team & Contributions

| Member | ID           | 
|---|--------------|
| Bitanya Damtew  | UGR/9112/16  |
|Lealem Tsehay | UGR/8016/16  | 
| Misgana Ashenafi | UGR/6355/16  |
| Nolawi Getye| UGR/1187/16  | 
| Selamawit Mengistu|  UGR/4008/16 | 

---

## Recording
There are 2 file in the folder based on the Addendum implemention
 **[Watch the demo here ](https://drive.google.com/drive/folders/1kNfJmwNtKXywczUQ9F9q6CfbehMXrkyH?usp=drive_link)**

---

